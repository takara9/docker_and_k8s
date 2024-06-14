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
$ git branch
```


## CIのワークフローを作成する
CI-TESTの下で、ワークフローのファイルの置くディレクトリを作成する
```
mkdir -p .github/workflows
```

Githubにpushされた後に、実行する作業を記述したファイルを配置します。
```
cd 4-7_CICD/1_Continous_Integration/
cp 4-7_CICD/1_Continous_Integration/ci.yaml .github/workflows
```

## ブランチしたディレクトリにファイルを作成する
ディレクトリ docker_and_k8s の直下に移動して、変更したディレクトリとファイルを追加して、コミットして、
クローンしたリポジトリへプッシュする。
```
$ cd ../../
$ git add .
$ git commit -m "test update"
$ git push --set-upstream origin ci-test
```

Webの画面に戻って、フォークしたリポジトリへPRを実施する
もし、フォーク元の　https://github.com/takara9/docker_and_k8s へプルリクを実施しても受け付けません。


## GitHub Actions のワークフローの実行を観察


