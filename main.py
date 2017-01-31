from cmd import Cmd

from code_maat import Project, ANALYSIS


class Shell(Cmd):
    prompt = ':'

    @staticmethod
    def do_inspect(git):
        """Generates stats for git repository given in parameters"""
        project = Project(git)

        print("Cloning project if it doesn't exist")
        project.clone()

        print("Generating logs")
        project.generate_logs()

        print("Parsing logs")

        for analysis in ANALYSIS:
            project.run_analysis(analysis=analysis)
        project.count_keyword(["add", "fix", "bug", "test", "refactor"])
        print("Analysis done")


if __name__ == '__main__':
    shell = Shell()
    shell.onecmd("inspect https://github.com/google/gson.git")
    shell.cmdloop()
