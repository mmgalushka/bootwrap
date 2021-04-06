# How to contribute to Bootwrap

Thank you for considering contributing to Bootwrap!


## Get Started


### Configure Git & Clone Repository

* Download and install the [latest version of git](https://git-scm.com/downloads).

* Configure git with your username and email.

```bash
~$ git config --global user.name 'your name'
~$ git config --global user.email 'your email'
```

* Create your [GitHub account](https://github.com/join) if you don't have one already.

* Fork Bootwrap to your GitHub account by clicking the Fork button.

* [Clone](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo#step-2-create-a-local-clone-of-your-fork) the main repository locally.

```bash
~$ git clone https://github.com/mmgalushka/bootwrap.git
~$ cd bootwrap
```

* Add fork as a remote where you will push your work to. Replace `{username}` with your username. 

```bash
~$ git remote add fork https://github.com/{username}/bootwrap
```


### Initialize Environment 

* Use `helper.sh` to create a virtual environment and initialize required dependencies.

```bash
~$ ./helper.sh init
```

**Note:**  `helper.sh` can be viewed as your "command centre". It allows performer various useful operations with the repository. Read this section to learn more about how to use the helper.

* Run test to make sure that all work well

```bash
~$ ./helper.sh test
```

It should be no error :wink:.


### Start Coding

* Create a branch to identify the issue you would like to work on. It is advisable to use the following convention for naming your issue: `issue-{number}`, where `number` is an issue identifier ex. `issue-123`. 

```bash
~$ git fetch origin
~$ git checkout -b your-branch-name origin/main
```

* Using your favorite editor to start coding. [Commit](https://dont-be-afraid-to-commit.readthedocs.io/en/latest/git/commandlinegit.html#commit-your-changes) changes regularly.

* Make sure you have all tests that cover any code changes you make. This project requires 100% coverage, no exception! 

```bash
~$ ./helper.sh test -c
```

* Push your commits to your fork on GitHub and create a [pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request). Link to the issue being addressed with `fixes #123` in the pull request.

```bash
$ git push --set-upstream fork your-branch-name
```
