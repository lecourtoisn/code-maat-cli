import os
from enum import Enum

from git import Repo

PROJECT_DIR = "projects"


class ANALYSIS(Enum):
    abs_churn = "abs-churn"
    age = "age"
    author_churn = "author-churn"
    authors = "authors"
    communication = "communication"
    coupling = "coupling"
    entity_churn = "entity-churn"
    entity_effort = "entity-effort"
    entity_ownership = "entity-ownership"
    fragmentation = "fragmentation"
    identity = "identity"
    main_dev = "main-dev"
    main_dev_by_revs = "main-dev-by-revs"
    messages = "messages"
    refactoring_main_dev = "refactoring-main-dev"
    revisions = "revisions"
    soc = "soc"
    summary = "summary"


class Project:
    def __init__(self, git_url):
        self.git_url = git_url
        self.name = git_url.split("/")[-1].split(".")[0]
        self.path = os.path.join(PROJECT_DIR, self.name)
        self.log_path = os.path.join(self.path, 'data.log')
        self.results = os.path.join(self.path, 'results')

    def clone(self, force=False):
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

    def count_keyword(self, keywords: list):
        results = {}
        for keyword in keywords:
            repo = Repo(self.path)
            commits = list(repo.iter_commits('master'))
            matching = [c.message for c in commits if keyword in c.message]
            results[keyword] = len(matching)

        with open(os.path.join(self.results, 'keywords.csv'), 'w+') as result_file:
            result_file.writelines(["{};{}\n".format(key, value) for key, value in results.items()])

    def _run_code_maat(self, output, **arguments):
        args = ' '.join(["-{} {}".format(arg, value) for arg, value in arguments.items()])
        cmd = ("java -jar code-maat-1.0-SNAPSHOT-standalone.jar -l {} {} -c git2 "
               "> {}".format(self.log_path, args, output))
        print(cmd)
        os.system(cmd)
