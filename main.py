import os
from cmd import Cmd

from code_maat import Project, ANALYSIS


class Shell(Cmd):
    prompt = ':'

    @staticmethod
    def do_retrieve(git):
        """Retrieve projects and perform code-maat analyses for git repository given in parameters"""
        project = Project(git)

        print("Cloning project if it doesn't exist")
        project.clone()

        print("Generating logs")
        project.generate_logs()

        print("Parsing logs")

        for analysis in ANALYSIS:
            project.run_analysis(analysis=analysis)
        print("Analysis done")

    @staticmethod
    def do_analyse(projects):
        """Aggregates code-mat raw data of specified projects to print statistics
        ex: analyse fitnesse gson"""
        if not projects:
            projects = os.listdir('projects')
        else:
            projects = projects.split(' ')

        print(projects)
        stats = [Project.age_routine, Project.age_routine_avg, Project.revisions_routine, Project.get_nb_commits,
                 Project.count_keyword]
        for stat in stats:
            print(stat.__name__)
            for project in projects:
                p = Project(folder_name=project)
                stat(p)
            print("_______________")


if __name__ == '__main__':
    shell = Shell()
    # shell.onecmd("retrieve https://github.com/google/gson.git")
    # shell.onecmd("analyse")
    # shell.onecmd("analyse fitnesse")
    # shell.onecmd("analyse fitnesse gson")
    shell.cmdloop()
