# GitHub lifecycle

## Instructor repository

The local project is independent of the course repository. Proposed remote name:
`computational-economics-lab`. Start private while reviewing the starter and choose
student access deliberately before release. No remote is configured by this starter.
Keep the course website's publication process separate.

Once the intended owner and visibility are chosen, create an **empty** repository
on GitHub (do not initialize a second README), then connect this existing project:

```sh
git remote add origin git@github.com:OWNER/computational-economics-lab.git
git status --short
git diff --check
git add README.md AGENTS.md CHANGELOG.md .gitignore pyproject.toml requirements.txt notes prompts docs src tests .github
git diff --cached --stat
git commit -m "Add cumulative Lab 6 and Lab 7 starter"
git push -u origin main
```

Replace OWNER with the intended account. If no Git author identity is configured,
set your own name/email locally before committing. Use an existing SSH setup or
HTTPS with a credential manager; never put a token into the remote URL or a file.
See [GitHub authentication](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github).

After review, mark the repository as a template in Settings if students should
create independent project histories. GitHub documents
[template setup](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository).
Template copies do not automatically receive later instructor updates. For this
workflow, issue later tasks as notes/prompts that students deliberately integrate.
Use forks instead when shared ancestry and upstream merges are a course requirement.
Do not mix the two workflows without explaining the update procedure.

## Student repository

Create your own repository from the released template, clone it, and create `.venv`
locally. Keep one repository for the rest of the course. Use a short branch such
as `lab07-growth`, commit reviewed changes in small steps, and merge only after
checks pass. Keep student work private when required by course submission rules;
no visibility policy is imposed here.

The supplied Actions workflow runs installation and tests on pushes and pull
requests. Once numerical tests are added, they join the same test discovery command.
A green workflow validates the scaffold and completed Lab 6; it does not validate
Lab 7 until its code and numerical tests are implemented. Consider requiring this check
before merges when the repository's account/plan supports that rule.

Use tags such as `lab06-complete` and `lab07-complete` only after the corresponding
experiments have been verified. Keep a short release description linking to the
notes and commands. Submit a commit SHA or tag rather than an unversioned folder.
