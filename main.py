from pprint import pprint
import os
from cmd import Cmd


class Shell(Cmd):
    prompt = ':'

    def do_generate(self, git):
        """Generates stats for git repository given in parameters"""
        name = git.split("/")[-1].split(".")[0]
        print("Checking repository existency")
        if not os.path.exists(name):
            print("Repository doesn't exist on disk, cloning")
            os.system("git clone {}".format(git))
            print("Done cloning")
        log_file = "{}/data.log".format(name)
        result_file = "{}/result_file.csv".format(name)
        print("Generating logs")
        os.system(
            "git -C {} log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames >{}".format(name,
                                                                                                                  log_file))
        print("Parsing logs")
        os.system("java -jar code-maat-1.0-SNAPSHOT-standalone.jar -l {} -c git2 > {}".format(log_file, result_file))
        print("Analysis done")

    def do_projects(self, projects):
        """Show projects"""
        folders = [d for d in os.listdir('.')]

        pprint(folders)


if __name__ == '__main__':
    shell = Shell()
    shell.cmdloop()
