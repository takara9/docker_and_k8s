GitHub Actionsで　CIを実施


mini:docker_and_k8s takara$ git checkout -b ci-test
Switched to a new branch 'ci-test'
mini:docker_and_k8s takara$ git branch
* ci-test
  main
mini:docker_and_k8s takara$ cp ~/work/deployment-ex5.yaml ./4-7_CICD/
mini:docker_and_k8s takara$ git status
On branch ci-test
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   .github/workflows/ci.yaml
        modified:   4-7_CICD/4-7-1_Continous_Integration/README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        4-7_CICD/deployment-ex5.yaml

no changes added to commit (use "git add" and/or "git commit -a")
mini:docker_and_k8s takara$ git add .
mini:docker_and_k8s takara$ git status
On branch ci-test
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   .github/workflows/ci.yaml
        modified:   4-7_CICD/4-7-1_Continous_Integration/README.md
        new file:   4-7_CICD/deployment-ex5.yaml

mini:docker_and_k8s takara$ git commit -m "test update"
[ci-test d6e1688] test update
 3 files changed, 48 insertions(+), 2 deletions(-)
 create mode 100644 4-7_CICD/deployment-ex5.yaml
mini:docker_and_k8s takara$ git push
fatal: The current branch ci-test has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin ci-test

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

mini:docker_and_k8s takara$ git push --set-upstream origin ci-test
Enumerating objects: 16, done.
Counting objects: 100% (16/16), done.
Delta compression using up to 8 threads
Compressing objects: 100% (5/5), done.
Writing objects: 100% (9/9), 940 bytes | 940.00 KiB/s, done.
Total 9 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
remote: 
remote: Create a pull request for 'ci-test' on GitHub by visiting:
remote:      https://github.com/takara9/docker_and_k8s/pull/new/ci-test
remote: 
To github.com:takara9/docker_and_k8s.git
 * [new branch]      ci-test -> ci-test
branch 'ci-test' set up to track 'origin/ci-test'.

