# 　継続的インテグレーション　 （CI）
GitHub Actionsで　CIを実施


## GitHubからforkする
自身のGitHubにログインして、https://github.com/takara9/docker_and_k8s をアクセスして、フォークする。


## CIの演習
このフォークしたリポジトリを、ローカル（パソコン）へクローンして、ディレクトリを移動する。
```
$ git clone git@github.com:takara8/docker_and_k8s.git
$ cd docker_and_k8s
```

git でブランチ ci-test を作る
```
$ git checkout -b ci-test
Switched to a new branch 'ci-test'
$ git branch
* ci-test
  main
```


## CIのワークフローを作成する
CI-TESTの下で、ワークフローのファイルの置くディレクトリを作成する
```
mkdir -p .github/workflow
```

Githubにpushされた後に、実行する作業を記述したファイルを配置します。
```
cp template/ci.yaml .github/workflow
```


## ブランチしたディレクトリにファイルを作成する
```
$ cp ~/work/deployment-ex5.yaml ./4-7_CICD/
$ git status
$ git add .
$ git status
```

```
$ git commit -m "test update"
$ git push
```

```
$ git push --set-upstream origin ci-test
```

## GitHub Actions のワークフローの実行を観察









maho-2:~ maho$ git clone git@github.com:takara8/docker_and_k8s.git
Cloning into 'docker_and_k8s'...
Enter passphrase for key '/Users/maho/.ssh/id_rsa': 
remote: Enumerating objects: 1399, done.
remote: Counting objects: 100% (71/71), done.
remote: Compressing objects: 100% (8/8), done.
remote: Total 1399 (delta 63), reused 69 (delta 63), pack-reused 1328
Receiving objects: 100% (1399/1399), 19.03 MiB | 6.75 MiB/s, done.
Resolving deltas: 100% (594/594), done.
maho-2:~ maho$ cd docker_and_k8s/
maho-2:docker_and_k8s maho$ ls
1-introduction          3-2_Commit_push         3-5_app_development     4-3_controller          4-6_Observability       work-temp
2-docker_run_and_remove 3-3_volume              4-1_pod_and_service     4-4_Scheduling          4-7_CICD
3-1_Run_and_stop        3-4_network             4-2_volume              4-5_network             README.md
maho-2:docker_and_k8s maho$ git checkout -b ci-test
Switched to a new branch 'ci-test'
maho-2:docker_and_k8s maho$ git branch
* ci-test
  main
maho-2:docker_and_k8s maho$ mkdir -p .github/workflow
maho-2:docker_and_k8s maho$ cd 4-7_CICD/1_Continous_Integration/
maho-2:1_Continous_Integration maho$ cp ci.yaml ../../.github/workflow/
maho-2:1_Continous_Integration maho$ git status
On branch ci-test
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        ../../.github/

nothing added to commit but untracked files present (use "git add" to track)
maho-2:1_Continous_Integration maho$ cd ../..
maho-2:docker_and_k8s maho$ git add .
maho-2:docker_and_k8s maho$ git status
On branch ci-test
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .github/workflow/ci.yaml

maho-2:docker_and_k8s maho$ git commit -m "update"
[ci-test 25b1e2e] update
 1 file changed, 34 insertions(+)
 create mode 100644 .github/workflow/ci.yaml
maho-2:docker_and_k8s maho$ git push
fatal: The current branch ci-test has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin ci-test

To have this happen automatically for branches without a tracking
upstream, see 'push.autoSetupRemote' in 'git help config'.

maho-2:docker_and_k8s maho$ git push --set-upstream origin ci-test
Enter passphrase for key '/Users/maho/.ssh/id_rsa': 
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 16 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (5/5), 850 bytes | 850.00 KiB/s, done.
Total 5 (delta 1), reused 1 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
remote: 
remote: Create a pull request for 'ci-test' on GitHub by visiting:
remote:      https://github.com/takara8/docker_and_k8s/pull/new/ci-test
remote: 
To github.com:takara8/docker_and_k8s.git
 * [new branch]      ci-test -> ci-test
branch 'ci-test' set up to track 'origin/ci-test'.
maho-2:docker_and_k8s maho$ 