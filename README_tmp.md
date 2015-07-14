Basically, this repository is from [here](https://github.com/naoa/docker-termextract)

# To set-up docker

```
% cd docker-termextract
% mkdir /var/lib/termextract
% docker build -t naoa/termextract .
```

# To login Docker container


```
% docker run -v /var/lib/termextract:/var/lib/termextract -i -t naoa/termextract /bin/bash
```


# To send json document and get analyzed json docuemnt

```
% cat ./dockerfiles/resources/received.json |\
docker run -v /var/lib/termextract:/var/lib/termextract \
-a stdin -a stdout -a stderr -i naoa/termextract python2.7 /analysis_code/docker_main.py
```

Input data is like below

```
{
    "inputArray": [
        "夜の10時過ぎにクラリネットの練習をする近所の中学生。上手ならまだしも、下手で耳ざわり。", 
        "家の中に数匹しかコバエがいないんだけど、なかなか殺せなくてイライラする。コバエがホイホイみたいなのを買うけどなかなか取れなくてさらにイライラ。クソくらいにコバエが飛んでるとこじゃないとコバエがホイホイは意味がない", 
        "不満買い取りでコツコツ売る私の旦那は1日でパチンコ5万負けてきます...(涙)", 
        "悪い事ばかりで泣きたくなる。疲れたー。", 
        "初めて行った美容院で、ドリンクサービスありとなってたのにカットだけだったからなのか知らないがくれなかった。暑いし、話しかけられるから余計喉渇くし欲しかった。", 
        "少量のチャーシューが無いので困る。欲しいのは数切れなのです。", 
        "インフルエンザが流行っていたのでしょう、ギチギチの中レジに並んでいて明らかに咳き込んでいる人がいました。数日後インフルエンザにかかりました。", 
        "レストランでビーフシチューを頼みました。激まずでした。肉は一口食べて吐きたかったけど、デートなので我慢。野菜は味が染み込んでない、というか、スープが不味いのでまだ食べれたかな。肉とスープは異常な不味さでした。ただの罰ゲーム", 
        "美容師さんとのトーク。疲れてしまう。雑誌を読みたいので施術に集中して欲しい。と言いたいけど言えない。", 
        "生ゴミの収集が週2回って少ない。生ゴミは毎日出るしせめて夏場はもう少し回数を増やしてほしい。", 
        "狭山ケ丘の若狭小学校前の道路につけた赤い棒を外すか、暗くてもはっきり見えるようにしてほしい。暗くなると街灯も少なく暗い為、何度か見えなくて棒にぶつかりひっくりかえってケガをしています。踏切前につけたのもかえって危ないです", 
        "改善提案を入力中に間違えて消そうとしても消えてくれず、何回試しても消えなかったから腹立って意味不明の文のまま投稿した。"
        ]
}
```

Analyzed result is like below. This document is returned with std out.

```
{
    "0": [
        [
            "夜", 
            [
                "名詞", 
                "副詞可能", 
                "*"
            ]
        ], 
        [
            "の", 
            [
                "助詞", 
                "連体化", 
                "*"
            ]
        ], 
        [
            "10", 
            [
                "名詞", 
                "固有名詞", 
                "一般"
            ]
        ], 
        [
            "時", 
            [
                "名詞", 
                "接尾", 
                "副詞可能"
            ]
        ], 
        [
            "過ぎ", 
            [
                "名詞", 
                "接尾", 
                "副詞可能"
            ]
        ], 
        [
            "に", 
            [
                "助詞", 
                "格助詞", 
                "一般"
            ]
        ], 
        [
            "クラリネット", 
            [
                "名詞", 
                "一般", 
                "*"
            ]
        ], 
        [
            "の", 
            [
                "助詞", 
                "連体化", 
                "*"
            ]
        ], 
        [
            "練習", 
            [
                "名詞", 
                "サ変接続", 
                "*"
            ]
        ], 
        [
            "を", 
            [
                "助詞", 
                "格助詞", 
                "一般"
            ]
        ], 
        [
            "する", 
            [
                "動詞", 
                "自立", 
                "*"
            ]
        ], 
        [
            "近所", 
            [
                "名詞", 
                "一般", 
                "*"
            ]
        ], 
        [
            "の", 
            [
                "助詞", 
                "連体化", 
                "*"
            ]
        ], 
        [
            "中学生", 
            [
                "名詞", 
                "一般", 
                "*"
            ]
        ], 
        [
            "。", 
            [
                "記号", 
                "句点", 
                "*"
            ]
        ], 
        [
            "上手", 
            [
                "名詞", 
                "形容動詞語幹", 
                "*"
            ]
        ], 
        [
            "だ", 
            [
                "助動詞", 
                "*", 
                "*"
            ]
        ], 
        [
            "まだしも", 
            [
                "副詞", 
                "一般", 
                "*"
            ]
        ], 
        [
            "、", 
            [
                "記号", 
                "読点", 
                "*"
            ]
        ], 

        .......omitted
```

# Use in production environment

This container saves learned data inside docker container.

Thus, it's better to use same container.

This is procedure to use same connector.

## Create shared folder

This direcotory will be used as shred folder between host-machine and docker container.

```
% sudo mkdir /var/lib/termextract
```

## Build image

```
% docker build -t naoa/termextract .
```

## Start container from image

```
% docker run -v /var/lib/termextract:/var/lib/termextract -i -t naoa/termextract /bin/bash
```

After checking this command works, you can log out from session with `exit`.

Next, you need to know container ID.

```
% docker ps -a                              
CONTAINER ID        IMAGE                     COMMAND                CREATED             STATUS                      PORTS               NAMES
36880ed4a975        naoa/termextract:latest   "/bin/bash"            4 minutes ago       Exited (0) 3 minutes ago                        pensive_hawking     
```

`36880ed4a975` is container ID here.

You need to re-start this container with following command.

```
docker start 36880ed4a975
```

When you checked container is re-running, type following command and test.

```
cat dockerfiles/resources/received.json |\
docker exec -i 1cb049204e0d python2.7 /analysis_code/docker_main.py
```

Analyzed result will be printed as Std.out

## Resource files

You can check generated dictionary csv at `/analysis_data/termExtractDict.csv`

You can get compiled binary MeCab dictionary at `/analysis_data/termExtractDict.dict`

## scripts inside docker 

A directory that has main process scripts.

* `data_connector.py`: connector that takes json document as Std input and returns json document as Std out.
* `wrapper_mecab.py`: a wrapper that calls MeCab system. This script uses a dictionary generated by `wrapper_termextract`
* `wrapper_termextract.py`: a wrapper script that calls termextract perl script
* `docker_main.py`: a main script that calls above 3 scripts


