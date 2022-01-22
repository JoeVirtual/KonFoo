# Contributing

**Version 0.0**

Welcome and thank you for your interest in contributing to the **KonFoo**
[project].

There are many ways to contribute, and we appreciate all of them.

- Feature Requests
- Bug Reports
- Pull Requests
- Writing Documentation

## Feature Requests

Feature requests need to go through a process to be approved by the team. Usually
this requires a "Final Comment Period" (FCP) or even a "Request for Comments"
(RFC).

## Bug Reports

While bugs are unfortunate, they're a reality in software. We can't fix what we
don't know about, so please report liberally. If you're not sure if something is
a bug or not, feel free to file a bug anyway.

If you have the chance, before reporting a bug, please search existing [issues],
as it's possible that someone else has already reported your error. This doesn't
always work, and sometimes it's hard to know what to search for, so consider
this extra credit. We won't mind if you accidentally file a duplicate report.

## Pull Requests

We recommend the git [forking workflow].

### Setting up your local environment

#### Step 1: Fork

Fork the [project] on [github.com] and clone your fork locally.

```shell
> git clone https://github.com/{username}/KonFoo.git
> cd KonFoo
```

Add a shorthand for the remote (`upstream`) repository of the forked [project]
and fetch the commits add to the remote (`upstream`) [project].

```shell
> git remote add upstream https://github.com/JoeVirtual/KonFoo.git
> git fetch upstream
```

Set your username and email for this [git] repository on your machine to
signature your commits

```shell
> git config user.name "your user name"
> git config user.email "your@email.com"
```

or for every [git] repository on your machine

```shell
> git config --global user.name "your user name"
> git config --global user.email "your@email.com"
```

#### Step 2: Build

The `konfoo` package requires at least [Python] 3.6.

```shell
> python setup.py install
```

In case the network firewall is blocking the installation set temporary the
environment variables for the HTTP network proxy on your machine to ensure that
the required Python packages can be installed from [PyPI] in your local [Python]
development environment.

```shell
> set HTTP_PROXY=http://<proxy>:<port>
> set HTTPS_PROXY=http://<proxy>:<port>
```

#### Step 3: Branch

To keep your development environment organized, create local branches to hold
your work. These should be branched directly off of the `master` branch.

```shell
> git checkout -b my-branch -t upstream/master
```

### Making changes

#### Step 4: Code

Follow the coding rules and coding style of the [project].

#### Step 5: Commit

Commit your changes using a descriptive commit message that follows our [commit
message conventions].

The cardinal rule for creating good commits is to ensure there is only one
"logical change" per commit.

Things to avoid when creating commits

- Mixing formatting changes with functional code changes.
- Mixing two unrelated functional changes.
- Sending large new features in a single giant commit.

```shell
> git commit --all
```

> *NOTE*: The optional commit `-a|--all` command line option will automatically
> "add" and "rm" edited files.

#### Step 6: Rebase

Once you have committed your changes, it is a good idea to use `git rebase`
(not `git merge`) to synchronize your work with the master branch of the
remote (`upstream`) repository of the forked [project].

```shell
> git fetch upstream
> git rebase upstream/master
```

This ensures that your working branch has the latest changes from `KonFoo`
master.

#### Step 8: Push

Once your commits are ready to go begin the process of opening a pull request
by pushing your working branch to your fork on [github.com].

```shell
> git push origin my-branch
```

#### Step 9: Opening the Pull Request

From within [github.com], opening a new [pull request] will present you
with a template that should be filled out.

#### Step 10: Discuss and update

You will probably get feedback or requests for changes to your [pull request].
This is a big part of the submission process so don't be discouraged! Some
stakeholders may sign off on the [pull request] right away. Others may have
detailed comments or feedback. This is a necessary part of the process in order
to evaluate whether the changes are correct and necessary.

To make changes to an existing [pull request], make the changes to your local
branch, add a new commit with those changes, and push those to your fork.
GitLab will automatically update the [pull request].

```shell
> git commit
> git push origin my-branch
```

#### Step 11: Landing

In order to land, a [pull request] needs to be reviewed and approved by at
least one [project] owner and pass CI. After that, if there are no objections
from other stakeholders, the [pull request] can be merged.

Congratulations and thanks for your contribution!

### Updating the commit message

A reviewer might often suggest changes to a commit message (for example, to add
more context for a change or adhere to our [commit message conventions]).
In order to update the commit message of the last commit on your branch:

1. Check out your branch:

    ```shell
    > git checkout my-branch
    ```

2. Amend the last commit and modify the commit message:

    ```shell
    > git commit --amend
    ```

3. Push to your [github.com] repository:

    ```shell
    > git push --force-with-lease
    ```

> *NOTE*: If you need to update the commit message of an earlier commit, you can
> use `git rebase` in interactive mode.

### After your Pull Request is merged

After your [pull request] is merged, you can safely delete your branch and pull
the changes from the remote (`upstream`) repository:

* Delete the remote branch on [github.com] either through the GitLab web
  UI, or your local shell as follows:

    ```shell
    > git push origin --delete my-branch
    ```

* Check out your `master` branch:

    ```shell
    > git checkout master -f
    ```

* Delete the local branch:

    ```shell
    > git branch -D my-branch
    ```

* Update your `master` with the latest `upstream` version:

    ```shell
    > git pull --ff upstream master
    ```

## Commit Message Conventions
[commit message conventions]: #commit-message-conventions

We use an adapted form of [conventional commits] for the git **commit messages**.

This leads to more readable **commit messages** that are easy to follow when
looking through the [project] history.

### Commit Message Format

Each **commit message** consists of a mandatory [header], an optional [body] and
optional [footer]s.

```text
<type>(<scope>)!: <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer(s)>
```

> *IMPORTANT*: Any line of the **commit message** shall not have more than 80
> characters!

### Header
[header]: #header

The [header], the first line in a **commit message**, has a special format that
includes a [type], an optional [scope], an optional [breaking change] indicator
`!` and a [subject]:

```text
<type>(<scope>)!: <subject>
```

```text
docs(CONTRIBUTING.md): add contributing guidelines
```

### Type
[type]: #type

The **commit message** [type] must be one of the following:

- `build:` Changes that affect the build system or external dependencies
- `chore:` Changes that affect the repository
- `ci:` Changes to continuous integration (CI) configuration files and scripts
- `docs:` Documentation only changes
- `feat:` A new feature
- `fix:` A bug fix
- `perf`:  A code change that improves performance
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `style:` Changes that do not affect the meaning of the code
- `test:` Adding missing tests or correcting existing tests

### Scope
[scope]: #scope

A [scope] may be provided after a [type]. A [scope] must consist of a noun
describing the affected *file*, the affected *section* in the codebase, or the
affected *chapter* in the documentation.

### Breaking Changes
[breaking change]: #breaking-changes

A commit that has the text `BREAKING-CHANGE:` at the beginning of its optional
[body] or [footer] section introduces a breaking API change. A [breaking change]
can be part of commits of any [type].

```text
refactor(trace)!: remove deprecated functions

BREAKING-CHANGES: <description>
```

### Subject
[subject]: #subject

The **commit message** [subject] line shall contain a short summary of the
changed subject.

Conventions for the [subject] line.

- use the imperative, present tense, like "change" not "changed" nor "changes"
- be entirely in lowercase except of proper nouns, acronyms, and the words that
  refer to code, like constant, function, enum variant, class, method, or
  attribute names
- no dot (.) at the end of the subject line

Good:
```text
docs(CONTRIBUTING.md): add contributing guidelines
```

Bad:
```text
docs(CONTRIBUTING.md): Added contributing Guidelines.
```

A properly formed commit [subject] line should always be able to complete the
following sentence:

> If applied, this commit will _<ins>your subject line here</ins>_.

For example:

- If applied, this commit will
  _<ins>refactor code segment for readability</ins>_.
- If applied, this commit will
  _<ins>update getting started documentation</ins>_.
- If applied, this commit will
  _<ins>remove deprecated function</ins>_.
- If applied, this commit will
  _<ins>release version 1.0.0</ins>_.

### Body
[body]: #body

A longer **commit message** [body] may be provided after the [subject],
providing additional contextual information about the changed [subject].

The [body] must begin one blank line after the [subject] in the [header].

### Footer
[footer]: #footer

The [footer] should contain any information about `BREAKING-CHANGES` and is also
the place to reference GitLab [issues] that this commit closes.

One or more [footer]s may be provided one blank line after the [body].

Each [footer] must consist of a word **token**, followed by either a `:<space>`
or `<space>#` separator, followed by a string value.

A [footer]’s **token** must use `-` in place of whitespace characters, this
helps differentiate the [footer] section from a multi-paragraph [body].

Examples:

```text
BREAKING-CHANGES: <description>
```

```text
Closes #{issue}
```

[Python]: https://www.python.org
[PyPI]: https://pypi.org
[semantic versioning]: https://semver.org
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0
[git]: https://git-scm.com
[git trailer format]: https://git-scm.com/docs/git-interpret-trailers
[forking workflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow
[github.com]: https://github.com
[issues]: https://github.com/JoeVirtual/KonFoo/issues
[project]: https://github.com/JoeVirtual/KonFoo
[pull request]: https://github.com/JoeVirtual/KonFoo/pulls
