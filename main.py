from pprint import pprint
import os
from cmd import Cmd

PROJECT_DIR = "projects"


class Shell(Cmd):
    prompt = ':'

    @staticmethod
    def do_inspect(git):
        """Generates stats for git repository given in parameters"""
        name = git.split("/")[-1].split(".")[0]
        path = "{}/{}".format(PROJECT_DIR, name)
        print("Checking repository existence")
        if not os.path.exists(path):
            print("Repository doesn't exist on disk, cloning")
            os.system("git clone {} {}".format(git, path))
            print("Done cloning")
        log_file = "{}/data.log".format(path)
        result_file = "{}/result_file.csv".format(path)
        print("Generating logs")
        os.system(
            ("git -C {} log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames"
             " >{}").format(path, log_file))
        print("Parsing logs")
        os.system("java -jar code-maat-1.0-SNAPSHOT-standalone.jar -l {} -c git2 > {}".format(log_file, result_file))
        print("Analysis done")

    @staticmethod
    def do_projects(projects):
        """Show projects"""
        folders = [f for f in next(os.walk(PROJECT_DIR))[1] if not f.startswith('.')]

        pprint(folders)


if __name__ == '__main__':
    shell = Shell()
    shell.cmdloop()
