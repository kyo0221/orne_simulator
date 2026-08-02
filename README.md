### Simulator
Ignition Gazeboのシミュレータ環境を提供します。

---
#### リファレンス
Ignition Gazebo
https://gazebosim.org/api/gazebo/6/tutorials.html

---
#### インストール
Binary Install（Ubuntu 18.04以上）
1. パッケージ リポジトリを構成します。
```
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt-get update
```
2. Ignition Gazeboをインストールします。
```
# <#>は6などの数値に置き換えてください。
sudo apt-get install libignition-gazebo<#>-dev 
sudo apt install ros-humble-ros-gz
```

---
#### 起動
```
ros2 launch orne_simulator gazebo_simulator.launch.py
```

launch引数:
- `world`: worlds/内のworldファイル名（デフォルト: `tsudanuma2-3_colors.sdf`）
- `verbosity`: Gazeboのログレベル（デフォルト: `1`）
- `use_sim_time`: シミュレーション時刻(/clock)の使用（デフォルト: `true`）

例:
```
ros2 launch orne_simulator gazebo_simulator.launch.py world:=orne_box_factory.sdf
```

ロボットのspawn位置は各worldファイル内のロボットの`<include>`の`<pose>`で定義します。

> **Note**: tsudanuma2-3の建物モデルはvisualのみでcollisionを持ちません（LiDAR・カメラには映りますが、物理的な衝突はしません）。

---
#### worldファイルからsdfファイルへの変換
```
gz sdf -p my_world.world > my_world_converted.sdf
```

---
## ライセンス表記

- `orne_box_factory.sdf` は、[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) ライセンスの下で提供されています。
© OpenRobotics
本ライセンスに基づき、適切なクレジットを表示し、変更を明記すれば、商用目的も含めて自由に利用・改変・再配布が可能です。

- [`tsudanuma2-3_colors.sdf`](https://github.com/masakifujiwara1/real_tsudanuma2-3_sim/tree/v2.1) に含まれるすべてのファイルは、[BSD 3-Clause "New" or "Revised" License](https://opensource.org/licenses/BSD-3-Clause) に基づいて配布されています。  
  © Masaki Fujiwara  
  このライセンスのもとで、ソフトウェアの再配布および使用は、ソースコード形式またはバイナリ形式であっても、以下の条件を満たす限り許可されます：
  - 元の著作権表示、条件一覧、免責事項を保持すること
  - 著作物の宣伝や推奨に、著作者の名前を使わないこと
