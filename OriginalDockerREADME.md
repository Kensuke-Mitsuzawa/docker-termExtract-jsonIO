# docker-termextract

専門用語（キーワード）自動抽出用Perlモジュール"TermExtract"をさらに簡単に使うためのDockerイメージを作成するDockerfileです。

元は前田朗氏が作成されていた[docker-termextract](https://github.com/naoa/docker-termextract)です。

変更点は下記です。

* 大量の文書を一気に処理できるように、I/Oをjsonにしている
* Web新語に強い[mecab-ipadic-neologd](https://github.com/neologd/mecab-ipadic-neologd)を利用している

TermExtractについては[このページ](http://gensen.dl.itc.u-tokyo.ac.jp/termextract.html)を参照してください。

* "TermExtract"のCOPYRIGHT
東京大学・中川裕志教授、横浜国立大学・森辰則助教授が 作成した「専門用語自動抽出システム」のExtract.pm を参考に、中川教授の 教示を受け、東京大学経済学部・前田朗が全面的に組みなおしたもの。(敬省略)   

このDockerfileでは、以下の環境のコンテナが構築されます。

| 項目        | バージョン | 備考 |
|:-----------|:------------|:------------|
| CentOS     | 7 | ja_JP.UTF-8|
| perl | 5.16.3 | yum base |
| python | 2.7 ||
| MeCab     | 0.996 | --enable-utf8-only |
| MeCab IPAdic | 2.7.0-20070801 |--with-charset=utf8|
| MeCab IPAdic model | 2.7.0-20070801 ||
| Mecab IPAdic neologd | 最新バージョンが随時適用 ||
| Mecab python | 0.996 ||
| MeCab perl | 0.996 ||
| TermExtract | 4_10 ||

## イメージ構築

```bash
% git clone git@github.com:
% cd docker-termextract
% mkdir /var/lib/termextract
% docker build -t termextract-json-io .
```

### docker host側の準備

コンテナと共有するディレクトリの用意

```
% mkdir /var/lib/termextract
```

## 使い方

### json fileの用意

"inputArray"というキーに対して、Arrayを置きます。

Arrayの中には１要素=１文で記述してください。

下記、例です。

```
{
    "inputArray": [
        "オットー・エドゥアルト・レオポルト・フュルスト（侯爵）・フォン・ビスマルク＝シェーンハウゼン（独: Otto Eduard Leopold Fürst von Bismarck-Schönhausen, 1815年4月1日 - 1898年7月30日）は、プロイセン及びドイツの政治家、貴族。プロイセン王国首相（在職1862年-1890年）、北ドイツ連邦首相（在職1867年-1871年）、ドイツ帝国首相（在職1871年-1890年）を歴任した。ドイツ統一の中心人物であり、「鉄血宰相（独: Eiserner Kanzler）」の異名を取る。",
        "アーヤトッラー・ルーホッラー・ホメイニー（آیت‌الله روح‌الله خمینی, Āyatollāh Rūhollāh Khomeinī, 1902年9月24日 - 1989年6月3日）は、イランにおけるシーア派の十二イマーム派の精神的指導者であり、政治家、法学者。1979年にパフラヴィー皇帝を国外に追放し、イスラム共和制政体を成立させたイラン革命の指導者で、以後は新生「イラン・イスラム共和国」の元首である最高指導者（師）として、同国を精神面から指導した。",
        "ホメイニーは、1902年にイラン中部のホメインの町でシーア派第7代イマーム、ムーサーの子孫を称するサイイド（預言者ムハンマドの直系子孫）の家系に生まれ、当初の名をルーホッラー・ムーサーヴィーといった。のちに「ホメイン出身の者」を意味するホメイニーを名乗る。",
        "希志 あいの（きし あいの、1988年2月1日 - ）は、日本のAV女優‎。元グラビアアイドル。東京都出身[1]、Duoエンターテイメント所属。実妹は元タレントの紗希せりか[2]。",
        "明日花 キララ（あすか キララ、1988年10月2日[1][2] - ）は、日本のAV女優。Diaz Planners所属。",
        "上原 亜衣（うえはら あい、1992年11月12日 - ）は、日本のAV女優。福岡県出身[3]、マインズ（mine's） 所属。",
        "スカウトをきっかけに2011年にAVデビュー[4]。「上原亜衣」という芸名は、当人が上原多香子と加藤あいに似ていることから所属事務所の社長が名付けた[5]。キャラは、天然で愛されキャラ[6]。特技は、軟体[1]。公式ブログの読者のことを「teamあいちん」と呼んでいる[7]。初体験は中学3年の夏に同級生の彼氏と彼氏の家で[8]。2013年12月1日に、AAK第4期生に選ばれ、「赤・青・黄」投票サイトで1位となった。DMMの2013年年間AV女優ランキングで1位となっている[9]2014年4月には、DMMアワード2014において最優秀女優賞プラチナを受賞した。2014年7月、セガのゲーム「龍が如く」のキャラクター出演をかけたセクシー女優人気投票にエントリー。[10][11][12] 2014年8月24日、結果発表。161,887票を集め3位に、「龍が如く」最新作への出演権を獲得した。[13]"
    ]
}
```

### コンテナ呼び出し

inputのjsonをcatコマンドで開いて、コンテナに送ります。

コンテナの`/analysis_code/docker_main.py`がjson文字列を受け取って処理をしてくれます。

```
% cat inputfile.json |\
docker run -v /var/lib/termextract:/var/lib/termextract \
-a stdin -a stdout -a stderr -i termextract-json-io python2.7 /analysis_code/docker_main.py
```





## Author



## License

Public domain. You can copy and modify this project freely.

