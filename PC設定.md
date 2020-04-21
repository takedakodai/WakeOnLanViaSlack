# Wake On Lan設定
  
## PC設定

### Windows内のWake On Lanを利用するための設定の確認修正

* デバイスマネージャーからネットワークアダプタ設定を確認。[参考1](https://n-archives.net/software/nwol/wol-pc-setting/windows-setting.html)[参考2](https://www.atmarkit.co.jp/ait/articles/0602/25/news014.html)
  1. ドライバーの更新が可能なら実行。
  2. 「詳細設定」からWake On Lanに関する設定を「有効」に変更。
  3. 「PMEをオンにする」を有効化へ変更。（選択肢があれば）
  4. 「電源の管理」の設定をすべてチェックへ変更。

* コントロールパネルから電源オプションの設定を確認。

  1. 「電源ボタンの動作の選択」から「現在利用可能ではない設定を変更します」をクリック。
  2. 「高速スタートアップを有効化する」のチェックを外す。
  3. 変更の保存。

### BIOS設定の確認修正

* このページを[参考](https://n-archives.net/software/nwol/wol-pc-setting/bios-setting-asrock.html)に基本設定を実行。
