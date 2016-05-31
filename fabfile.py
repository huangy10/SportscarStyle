from fabric.api import run, cd, sudo, env, prompt
from fabric.contrib.files import exists

env.hosts = ["scs_runner@paochefan.com:22"]
env.password = ["shanghai"]


def deploy():
    prompt("Push you local change to github before deployment!\n(Press any key to continue)")

    with cd("/home/scs_runner"):
        if not exists("./SportscarStyle"):
            print "Project not fond, cloning from github"
            run("git clone https://github.com/huangy10/SportscarStyle.git")
    with cd("/home/scs_runner/SportscarStyle"):
        print "Update source code from github"
        run("git checkout")
        run("git pull origin master")
        print "Applying server settings"
        run("rm SportscarStyle/settings.py")
        run("rm SportscarStyle/settings_remote.py")
        #
        migrate_db = prompt("Did you modify the database? [Y/n]", validate=r'[YNyn]')
        if migrate_db in ["Y", "y"]:
            run("workon scs_env && python manage.py makemigrations")
            run("workon scs_env && python manage.py migrate")
        # restart server
        print "Restarting server"
        sudo("supervisorctl restart SportscarStyle SportscarStyle_chat scs_celery")
