# Python3 library for I2C Servo Motor Driver PCA9685

サーボモータードライバ PCA9685用 Python3ライブラリ

## ServoPCA9685

* 複数のサーボを同時に制御できる。


## 動作環境

* 本体: Raspberry Pi
* モータードライバー: PCA9685
* サーボモーター: SG-90 (および互換品)
* プログラミング言語: Python3
* GPIO制御ライブラリ: pigpio

## 0. TL;DR

```bash
$ cd ~
$ python3 -m venv env1
$ cd env1
$ . ./bin/activate
(env1)$ git clone https://github.com/ytani01/ServoPCA9685.git
(env1)$ cd ServoPCA9685
(env1)$ pip3 install -r requirements.txt
(env1)$ sudo pigpiod
(env1)$ ./ServoPCA9685.py -h
```

## 1. INSTALL

### 1.1 create python3 virtualenv

```bash
$ cd
$ python3 -m venv env1
$ cd env1
$ . bin/activate
```

### 1.2 clone git repository

```bash
$ cd ~/env1
$ git clone https://github.com/ytani01/ServoPCA9685.git
```

### 1.3 execute setup.sh

```bash
$ cd ~/env1/music-box
$ . ../bin/activate
$ ./setup.sh
```

## 2. SAMPLE and USAGE

see usage

```bash
$ ./ServoPCA9685.py -h
```


## A. 参考

* [pigpio/Examples/Python code](http://abyz.me.uk/rpi/pigpio/examples.html#Python%20code)
