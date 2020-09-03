# I2C Servo Motor Driver PCA9685

# TODO

* pigpio版に切り替える
[pigpio/Examples/Python code](http://abyz.me.uk/rpi/pigpio/examples.html#Python%20code)


## 1. install

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

$ git clone git@github.com:ytani01/servo-PCA9685.git
or 
$ git clone https://github.com/ytani01/servo-PCA9685.git
```

### 1.3 execute setup.sh

```bash
$ cd ~/env1/music-box
$ . ../bin/activate
$ ./setup.sh
```

## 2. sample and usage

see usage

```bash
$ ./ServoPCA9685.py -h
```
