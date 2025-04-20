# How to contribute to Bootwrap

Thank you for considering contributing to Bootwrap!

## Get Started

### Configure Git & Clone Repository

* Download and install the [latest version of git](https://git-scm.com/downloads).

* Configure git by setting up your username and email.

```bash
~$ git config --global user.name 'your name'
~$ git config --global user.email 'your email'
```

* Create your [GitHub account](https://github.com/join) if you don't have one already.

* Fork Bootwrap to your GitHub account using the Fork button.

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
~$ ./helper.sh test
```

* Push your commits to your fork on GitHub and create a [pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request). Link to the issue being addressed with `fixes #123` in the pull request.

```bash
~$ git push --set-upstream fork your-branch-name
```

## Helper Usage

`helper.sh` provides a command-line shell to automate a lot of routine operations. To see the available commands call `helper.sh` without options.

```text
~$ ./helper.sh

    ____              __ _       __                
   / __ )____  ____  / /| |     / /________ _____  
  / __  / __ \/ __ \/ __/ | /| / / ___/ __ '/ __ \ 
 / /_/ / /_/ / /_/ / /_ | |/ |/ / /  / /_/ / /_/ / 
/_____/\____/\____/\__/ |__/|__/_/   \__,_/ .___/  
Python + Bootstrap                       /_/       

System Commands:
   init initializers environment;
   test ... runs tests;
      -m <MARK> runs tests for mark;
      -c generates code coverage summary;
      -r generates code coverage report;
   preview runs web-server with documentation preview;
   docs generates documentation (HTML-pages);
   demo runs web-server with showcase project;
   build generates distribution archives;
```

### Init

`init` command performs initialization of Bootwrap project from scratch. Usually, it should be called just once  (straight after cloning repository).  First, it creates a virtual environment and installs necessary dependencies defined in the `requirements.txt` file. If you introduce a new dependency (to `requirements.txt` file) run the `init` command again.

### Test

`test` command helps to test Bootwrap project using `pytest`. It can be run with the following option.

| Option      | Description |
|:-----------:|:------------|
| -m \<MARK\> | runs tests for MARK |
| -c          | generates code coverage summary (% of tested code) |
| -r          | generates code coverage report (to see what is covered by tests and what is not) |

More information about code coverage can be found [here](https://pytest-cov.readthedocs.io/en/latest/).

During development, you might need to work on a specific web component. If you wish to run the test for just one component only use the `-m` option,  followed by the marker name. The maker name defines what component should be tested. For example, the following command will run testa for the Button web component.

 ```bash
~$ ./helper.sh test -m button
```

You can find a list of all available markers in the `pytest.ini` file.

---  
  NOTE

  This project requires 100% coverage! Please make sure  you introduced all necessary tests, before launching a pull request. Just run test command with coverage option `-c`.

 ```bash
~$ ./helper.sh test -c
  ```

---

### Preview

Use the `preview` command to launch Flask web-server with documentation.  The Bootwrap documentation is not just a place describing class/methods and their usage. It is a project showcase of how each component can be used and how it looks like.  

```bash
~$ ./helper.sh preview
```

Follow the link `http://127.0.0.1:5000/` to see the documentation in action.

### Docs

Run the `docs` command to generate static HTML pages with the project documentation under `docs` folder. It is advisable to run this command before pushing your code to origin. This way, your documentation will be available via GitHub pages.

```bash
~$ ./helper.sh docs
```

### Demo

Use the `demo` command to launch Flask web-server with show-case project. This project allows users to see how the Bootwrap library can be used for creating applications with a rich web interface.

```bash
~$ ./helper.sh preview
```

Follow the link `http://127.0.0.1:5000/` to see the demo in action.

### Build

Run the `build` command to package the Bootwrap project for PIP installation. This command should be most used by the repository administrator. However, it would be also useful for testing the Bootwrap package installation on the local machine.  

```bash
~$ ./helper.sh build
```
