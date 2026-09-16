# Git Fundamentals — Professional Workflow

A practical Git revision guide covering the commands and concepts required to move from basic Git usage to a professional team workflow.

---

# 🟢 Phase 1 — Git Fundamentals

## 1. `git status`

Shows the current state of your repository.

```bash
git status
```

It tells you:

* Current branch
* Modified files
* Untracked files
* Staged files
* Whether your branch is ahead/behind the remote

Example:

```text
nothing to commit, working tree clean
```

This means there are no uncommitted changes.

### Professional habit

Run this frequently, especially before:

```bash
git add
git commit
git pull
git push
```

---

# 2. `git log`

Shows commit history.

```bash
git log
```

Compact version:

```bash
git log --oneline
```

Last 5 commits:

```bash
git log --oneline -5
```

Recommended view:

```bash
git log --oneline --graph --decorate --all
```

Example:

```text
d508262 (HEAD -> master, origin/master) finally understood whole dl workflow
33652cf trained my first neural network
bab12b2 deeplearning finally updated
1336f37 learning updated
ed3b563 some dbms updates
```

### Understanding the output

```text
d508262
```

Commit hash.

```text
HEAD
```

Represents your current position in Git history.

```text
master
```

Your current local branch.

```text
origin/master
```

Your local reference to the remote `master` branch.

If both point to the same commit:

```text
master
   ↓
d508262
   ↑
origin/master
```

your local branch and remote-tracking branch are synchronized.

---

# 3. `git show`

Shows information about a specific commit.

```bash
git show <commit-hash>
```

Example:

```bash
git show d508262
```

Shows:

* Commit information
* Author
* Commit message
* Files changed
* Actual code changes

You can also inspect the latest commit:

```bash
git show HEAD
```

---

# 4. `git diff`

Shows differences between versions of your files.

```bash
git diff
```

This shows changes that are:

```text
Working Directory
        ↓
NOT staged yet
```

Example workflow:

```bash
# Modify a file

git diff
```

You can inspect exactly what changed before staging it.

### Staged changes

```bash
git diff --staged
```

This shows changes that have already been added to the staging area.

Mental model:

```text
File modified
     ↓
git diff
     ↓
Review changes
     ↓
git add
     ↓
git diff --staged
     ↓
Review staged changes
     ↓
git commit
```

---

# 5. `git remote`

Shows connected remote repositories.

```bash
git remote -v
```

Example:

```text
origin  https://github.com/user/project.git (fetch)
origin  https://github.com/user/project.git (push)
```

`origin` is the conventional name given to the main remote repository.

### Add a remote

```bash
git remote add origin <repository-url>
```

### Remove a remote

```bash
git remote remove origin
```

### Rename a remote

```bash
git remote rename origin upstream
```

---

# 6. `git add`

Moves changes into the staging area.

```bash
git add filename
```

Example:

```bash
git add app.py
```

Add multiple files:

```bash
git add app.py README.md
```

Add everything:

```bash
git add .
```

### Interactive staging

```bash
git add -p
```

Allows you to select individual changes instead of staging an entire file.

---

# 7. `git commit`

Creates a permanent snapshot of staged changes.

```bash
git commit -m "Add authentication"
```

A good commit should represent one logical change.

### Conventional Commit style

```text
feat: add authentication
fix: handle invalid login
refactor: simplify user service
docs: update README
test: add authentication tests
chore: update dependencies
```

Avoid commits like:

```text
update
changes
final
stuff
test
asdf
```

---

# 8. `git push`

Uploads local commits to the remote repository.

```bash
git push
```

First push of a new branch:

```bash
git push -u origin feature/login
```

The `-u` establishes an upstream relationship.

After that:

```bash
git push
```

is usually enough.

---

# 🟡 Phase 2 — Branching

Branches allow multiple lines of development to exist independently.

Example:

```text
                 feature/login
                /
main ----------A---------B
```

Instead of directly modifying `main`, professional development commonly uses feature branches.

---

# 9. `git branch`

List local branches:

```bash
git branch
```

List all branches:

```bash
git branch -a
```

List remote branches:

```bash
git branch -r
```

Create a branch:

```bash
git branch feature/login
```

Delete a branch:

```bash
git branch -d feature/login
```

Force delete:

```bash
git branch -D feature/login
```

---

# 10. `git switch`

Switch between branches.

```bash
git switch main
```

Create and switch to a new branch:

```bash
git switch -c feature/login
```

Example:

```bash
git switch main

git switch -c feature/auth
```

Now:

```text
main
  \
   feature/auth ← HEAD
```

### Older alternative

You may also encounter:

```bash
git checkout feature/auth
git checkout -b feature/auth
```

Modern Git separates branch switching into `git switch`, which is easier to understand.

---

# 11. Professional Branch Naming

Use descriptive names.

Good:

```text
feature/user-auth
feature/product-search
feature/recommendation-api

bugfix/login-error
bugfix/payment-error

hotfix/security-patch

refactor/recommendation-service
```

Avoid:

```text
branch1
test
newbranch
ahmad
final
final2
new-feature
```

---

# 12. `git merge`

Combines changes from one branch into another.

Suppose:

```text
main
A---B

feature
A---B---C---D
```

Switch to `main`:

```bash
git switch main
```

Merge the feature:

```bash
git merge feature
```

Result:

```text
A---B---C---D
            ↑
           main
```

Depending on the history, Git may create a merge commit.

---

# 13. Fast-Forward Merge

If the target branch hasn't changed:

```text
main:
A---B

feature:
A---B---C---D
```

Git can simply move `main` forward:

```text
A---B---C---D
            ↑
           main
```

This is called a **fast-forward merge**.

---

# 14. Merge Conflicts

A conflict occurs when Git cannot automatically determine which change should be kept.

Example:

```text
<<<<<<< HEAD
print("Hello")
=======
print("Hi")
>>>>>>> feature/login
```

You manually edit the file to the desired result.

Then:

```bash
git add filename
```

Complete the merge:

```bash
git commit
```

### Abort a merge

```bash
git merge --abort
```

This returns the repository to its state before the merge.

---

# 🟡 Phase 3 — Remote Synchronization

Understanding the difference between:

```text
fetch
pull
push
```

is extremely important.

---

# 15. `git fetch`

Downloads information about changes from a remote repository without modifying your current working branch.

```bash
git fetch origin
```

Fetch everything:

```bash
git fetch --all
```

Remove references to deleted remote branches:

```bash
git fetch --prune
```

Recommended:

```bash
git fetch --all --prune
```

Mental model:

```text
GitHub
   ↓
git fetch
   ↓
origin/main
```

Your local files are not automatically changed.

---

# 16. `git pull`

Gets remote changes and integrates them into your current branch.

```bash
git pull
```

Conceptually:

```text
git fetch
+
git merge
```

Depending on configuration, pull can also use rebase.

A common professional workflow is:

```bash
git pull --rebase
```

---

# 17. `git push`

Sends your local commits to the remote repository.

```bash
git push
```

First push:

```bash
git push -u origin feature/login
```

After upstream tracking is configured:

```bash
git push
```

---

# 18. `git branch -vv`

Shows tracking information.

```bash
git branch -vv
```

Example:

```text
* feature/login abc123 [origin/feature/login] Add login
  main          d508262 [origin/main] Update README
```

This helps determine which remote branch your local branch is tracking.

---

# 19. Fetch vs Pull

### Fetch

```bash
git fetch
```

Download remote information.

Does NOT directly merge the changes into your current branch.

### Pull

```bash
git pull
```

Fetch + integrate changes.

### Push

```bash
git push
```

Send your local commits to the remote.

Mental model:

```text
             GitHub
             /    \
        fetch      push
          ↓          ↑
       Local Git Repository
              ↓
             pull
```

---

# 20. Typical Synchronization Workflow

Before starting new work:

```bash
git switch main
git pull --rebase origin main
```

Then create your feature branch:

```bash
git switch -c feature/recommendation-api
```

---

# 🔴 Phase 4 — Undoing Mistakes & Recovery

This phase is about understanding what to do when something goes wrong.

The most important commands:

```text
git restore
git revert
git reset
git reflog
git stash
```

---

# 21. `git restore`

Discard changes in a file that have NOT been committed.

```bash
git restore filename
```

Example:

```bash
git restore app.py
```

Discard all unstaged changes:

```bash
git restore .
```

⚠️ This can permanently discard your uncommitted changes.

---

# 22. Unstage a File

If you accidentally run:

```bash
git add app.py
```

you can remove it from staging:

```bash
git restore --staged app.py
```

The changes remain in your working directory.

Mental model:

```text
Before:

Working Directory
       ↓
     Changes
       ↓
Staging Area
```

After:

```text
git restore --staged app.py

Working Directory
       ↓
     Changes

Staging Area
       ↓
     Empty
```

---

# 23. `git revert`

Safely undo an existing commit by creating a NEW commit.

```bash
git revert <commit-hash>
```

Example:

```bash
git revert d508262
```

History becomes:

```text
A---B---C---D
        ↑
       bad

A---B---C---D---E
                ↑
        revert of D
```

The original commit remains in history.

### Professional use

Use `git revert` when the commit has already been pushed/shared and you want to undo its effect without rewriting shared history.

---

# 24. `git reset`

Moves the current branch pointer backward.

```bash
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
```

---

## `--soft`

```bash
git reset --soft HEAD~1
```

Removes the last commit but keeps the changes staged.

```text
Commit       ❌
Staging      ✅
Working      ✅
```

Useful when you want to redo a commit.

---

## `--mixed`

```bash
git reset --mixed HEAD~1
```

Removes the commit and unstages the changes.

```text
Commit       ❌
Staging      ❌
Working      ✅
```

This is the default reset mode.

---

## `--hard`

```bash
git reset --hard HEAD~1
```

Moves the branch backward and discards working/staged changes associated with the removed commits.

```text
Commit       ❌
Staging      ❌
Working      ❌
```

⚠️ Dangerous. Do not use casually.

---

# 25. `HEAD`

`HEAD` represents your current position in Git.

Example:

```text
A---B---C
        ↑
       HEAD
```

Previous commit:

```bash
git show HEAD~1
```

Two commits back:

```bash
git show HEAD~2
```

Move back one commit:

```bash
git reset HEAD~1
```

---

# 26. `git reflog`

`reflog` records movements of `HEAD` and branch references.

```bash
git reflog
```

It is extremely useful for recovering from accidental operations.

Example:

```text
git reset --hard HEAD~3
```

You realize that you removed important commits.

Check:

```bash
git reflog
```

Find the previous commit:

```text
abc123 HEAD@{1}: reset: moving to HEAD~3
def456 HEAD@{2}: commit: important work
```

Recover:

```bash
git reset --hard def456
```

Think of reflog as Git's recovery mechanism.

---

# 27. `git stash`

Temporarily saves uncommitted changes.

Example situation:

```text
You're working on feature/payment.

Your code isn't finished.

A production bug needs immediate attention.
```

Save your work:

```bash
git stash
```

Switch branches:

```bash
git switch main
```

Do the urgent work.

Return:

```bash
git switch feature/payment
```

Restore your work:

```bash
git stash pop
```

---

# 28. Stash Commands

Create stash:

```bash
git stash
```

Create named stash:

```bash
git stash push -m "WIP payment integration"
```

List stashes:

```bash
git stash list
```

Apply stash:

```bash
git stash apply
```

Apply a specific stash:

```bash
git stash apply stash@{1}
```

Apply and remove from stash list:

```bash
git stash pop
```

Delete stash:

```bash
git stash drop stash@{1}
```

Delete all stashes:

```bash
git stash clear
```

---

# 29. `git clean`

Removes untracked files.

Preview first:

```bash
git clean -n
```

Actually remove:

```bash
git clean -f
```

Remove untracked directories too:

```bash
git clean -fd
```

⚠️ Always use `-n` first to see what will be deleted.

---

# 30. Reset vs Revert

This is a critical distinction.

### Reset

Moves history backward.

```bash
git reset
```

Can rewrite local history.

### Revert

Creates a new commit that reverses an old commit.

```bash
git revert
```

Does not remove the original commit.

### Practical rule

For commits that are already shared/pushed:

```text
Prefer revert
```

For local commits that haven't been shared:

```text
reset can be appropriate
```

---

# 🔥 Professional Git Workflow

A typical feature-development workflow:

## 1. Update main

```bash
git switch main
git pull --rebase origin main
```

## 2. Create feature branch

```bash
git switch -c feature/user-auth
```

## 3. Write code

```text
Implement feature
Run tests
Fix bugs
```

## 4. Inspect changes

```bash
git status
git diff
```

## 5. Stage

```bash
git add .
```

## 6. Review staged changes

```bash
git diff --staged
```

## 7. Commit

```bash
git commit -m "feat: add user authentication"
```

## 8. Push

```bash
git push -u origin feature/user-auth
```

## 9. Create Pull Request

```text
feature/user-auth
        ↓
      GitHub
        ↓
   Pull Request
        ↓
   Code Review
        ↓
    CI / Tests
        ↓
      Merge
        ↓
      main
```

## 10. Clean up

After the feature is merged:

```bash
git switch main
git pull --rebase origin main
git branch -d feature/user-auth
```

---

# 🧠 Commands to Master by Phase

## Phase 1 — Fundamentals

```bash
git status
git log
git show
git diff
git remote -v
git add
git commit
git push
```

---

## Phase 2 — Branching

```bash
git branch
git switch
git switch -c
git merge
git branch -d
```

---

## Phase 3 — Remote Synchronization

```bash
git fetch
git pull
git push
git branch -vv
git fetch --prune
```

---

## Phase 4 — Recovery

```bash
git restore
git restore --staged
git stash
git revert
git reset
git reflog
git clean
```

---

# 🎯 Practice Progression

Do not just memorize these commands.

Practice them in a repository.

### Exercise 1

```text
Modify a file
↓
git status
↓
git diff
↓
git add
↓
git diff --staged
↓
git commit
↓
git log
```

### Exercise 2

```text
Create feature branch
↓
Make changes
↓
Commit
↓
Switch main
↓
Merge feature
```

### Exercise 3

```text
Create a merge conflict
↓
Resolve it manually
↓
Commit the resolution
```

### Exercise 4

```text
Create commits
↓
Use git reset
↓
Use git reflog
↓
Recover the previous state
```

### Exercise 5

```text
Modify files
↓
git stash
↓
Switch branch
↓
Do other work
↓
Return
↓
git stash pop
```

---

# 🏆 Core Mental Model

Remember this:

```text
                 WORKING DIRECTORY
                        │
                     git add
                        ↓
                 STAGING AREA
                        │
                   git commit
                        ↓
                LOCAL REPOSITORY
                        │
                    git push
                        ↓
                REMOTE REPOSITORY
```

Getting changes:

```text
REMOTE REPOSITORY
       │
   git fetch
       ↓
REMOTE-TRACKING BRANCH
       │
 git merge/rebase
       ↓
LOCAL BRANCH
```

Undoing:

```text
restore → discard working changes

stash   → temporarily save changes

revert  → safely undo a shared commit

reset   → move local history

reflog  → recover lost Git states
```

---

# Final Professional Workflow

The goal is not to memorize every Git command.

The goal is to reach the point where you can look at a situation and think:

```text
"What state is my repository in?"
            ↓
       git status
            ↓
"What exactly changed?"
            ↓
        git diff
            ↓
"Should this become a commit?"
            ↓
        git add
            ↓
        git commit
            ↓
"Does remote have newer work?"
            ↓
     git fetch/pull
            ↓
"Where should this work live?"
            ↓
        git branch
            ↓
"What if histories diverge?"
            ↓
     merge / rebase
            ↓
"What if I screw up?"
            ↓
restore / revert / reset / reflog
```

That is the foundation of professional Git usage.
