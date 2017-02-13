import os
from enum import Enum
import csv

import math
from pprint import pprint

from git import Repo

PROJECT_DIR = "projects"


class ANALYSIS(Enum):
    age = "age"
    coupling = "coupling"
    fragmentation = "fragmentation"
    identity = "identity"
    revisions = "revisions"
    soc = "soc"
    # abs_churn = "abs-churn"
    # author_churn = "author-churn"
    # authors = "authors"
    # communication = "communication"
    # entity_churn = "entity-churn"
    # entity_effort = "entity-effort"
    # entity_ownership = "entity-ownership"
    # main_dev = "main-dev"
    # main_dev_by_revs = "main-dev-by-revs"
    # messages = "messages"
    # refactoring_main_dev = "refactoring-main-dev"
    # summary = "summary"


class Project:
    def __init__(self, git_url=None, folder_name=None):
        self.git_url = git_url
        self.name = git_url.split("/")[-1].split(".")[0] if git_url is not None else folder_name
        self.path = os.path.join(PROJECT_DIR, self.name)
        self.log_path = os.path.join(self.path, 'data.log')
        self.results = os.path.join(self.path, 'results')

    def clone(self, force=False):
        if not self.git_url:
            raise Exception("Url unknown")
        if force or not os.path.exists(self.path):
            os.system("git clone {} {}".format(self.git_url, self.path))
        if not os.path.exists(self.results):
            os.mkdir(self.results)

    def generate_logs(self):
        os.system("git -C {} log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames >{}"
                  .format(self.path, self.log_path))

    def run_analysis(self, analysis: ANALYSIS = None, output=None):
        analysis = analysis or ANALYSIS.summary
        output = output or "{}{}".format(analysis.value, '.csv')
        output = os.path.join(self.results, output)
        self._run_code_maat(output, a=analysis.value)

    def count_keyword(self, keywords: list = None):
        keywords = keywords or ["add", "fix", "bug",
                                "test", "refactor", "issue", "remove", "rm",
                                ]
        results = {}
        for keyword in keywords:
            repo = Repo(self.path)
            commits = list(repo.iter_commits('master'))
            matching = [c.message for c in commits if keyword in c.message]
            results[keyword] = len(matching)
        print("{:10} {}".format(self.name, ', '.join(["{} {:10}".format(key, "{}%({})".format(int(value*100/len(commits)), value)) for key, value in results.items()])))

    def _run_code_maat(self, output, **arguments):
        args = ' '.join(["-{} {}".format(arg, value) for arg, value in arguments.items()])
        cmd = ("java -jar code-maat-1.0-SNAPSHOT-standalone.jar -l {} {} -c git2 "
               "> {}".format(self.log_path, args, output))
        print(cmd)
        os.system(cmd)

    def get_result(self, analysis):
        return os.path.join(self.results, "{}.csv".format(analysis))

    def result_iterator(self, analysis):
        with open(self.get_result(analysis)) as file:
            file = csv.DictReader(file)
            for row in file:
                yield row

    def age_routine(self):
        nb_files = 0
        recent_files = 0
        for row in self.result_iterator("age"):
            path, age = os.path.join(self.path, row['entity']), int(row['age-months'])
            if not os.path.exists(path):
                continue
            nb_files += 1
            if age <= 2:
                recent_files += 1
        print("{:10}{:6}{:6}{:6}%".format(self.name, recent_files, nb_files, math.floor(recent_files * 100 / nb_files)))

    def age_routine_avg(self):
        max_age = max(int(x['age-months']) for x in self.result_iterator("age"))
        percents = [int(x['age-months'])/max_age for x in self.result_iterator("age")]
        average = sum(percents) * 100 / len(percents)
        print("{:10} {:3.2f}%".format(self.name, average))

    def revisions_routine(self):
        # revisions = [row['n-revs'] for row in self.result_iterator("revisions")]
        revisions = list(self.result_iterator("revisions"))
        get_revisions = lambda x: int(x['n-revs'])
        max_rev = max(revisions, key=get_revisions)
        avg_rev = sum([get_revisions(a) for a in revisions]) / len(revisions)
        print("{:10}{:6}{:6.2f}".format(self.name, get_revisions(max_rev), avg_rev))

    def get_nb_commits(self):
        repo = Repo(self.path)
        print(self.name, len(list(repo.iter_commits('master'))))
