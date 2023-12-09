import logging
import subprocess
import glob
import os
from helpers import get_homebrew_path

#日志配置
try:
    LOG_LOCATION = "/tmp/PowerControl_py.log"
    logging.basicConfig(
        level = logging.INFO,
        filename = LOG_LOCATION,
        format="[%(asctime)s | %(filename)s:%(lineno)s:%(funcName)s] %(levelname)s: %(message)s",
        filemode = 'w',
        force = True)
except Exception as e:
    logging.error(f"日志配置异常|{e}")

#路径配置
try:
    HOMEBREW_PATH = get_homebrew_path()   
    SH_PATH="{}/plugins/PowerControl/backend/sh_tools.sh".format(HOMEBREW_PATH)
    RYZENADJ_PATH="{}/plugins/PowerControl/bin/ryzenadj".format(HOMEBREW_PATH)
    GPU_DEVICE_PATH = glob.glob("/sys/class/drm/card?/device")[0]
    GPUFREQ_PATH = "{}/pp_od_clk_voltage".format(GPU_DEVICE_PATH)
    GPULEVEL_PATH = "{}/power_dpm_force_performance_level".format(GPU_DEVICE_PATH)
except Exception as e:
    logging.error(f"路径配置异常|{e}")

#设备信息获取配置
try:
    command="sudo sh {} get_cpuID ".format(SH_PATH)
    CPU_ID=subprocess.getoutput(command)
    PRODUCT_NAME = open("/sys/devices/virtual/dmi/id/product_name", "r").read().strip()
except Exception as e:
    logging.error(f"设备信息配置异常|{e}")

#TDP上限配置
try:
    TDP_LIMIT_CONFIG_PRODUCT={
        "AIR":18,
        "AIR 1S":25,
        "AIR Pro":20,
        "AIR Plus":30,
        "AYANEO 2":30,
        "GEEK":30,
        "GEEK 1S":30,
        "AYANEO 2S":30,
        "ONEXPLAYER Mini":30,
        "NEXT":35,
        "ONEXPLAYER Mini Pro":40,
        "AOKZOE A1 AR07":40,
        "ONEXPLAYER 2 ARP23":45,
        "G1619-04":45,     #GPD WINMAX2
        "G1618-04":45,     #GPD WIN4
        "G1617-01":30,    #GPD WIN mini
        "ROG Ally RC71L_RC71L":40,
        "Jupiter":20,
    }
    TDP_LIMIT_CONFIG_CPU={
        "AMD Ryzen 7 7735HS with Radeon Graphics":45,
        "AMD Ryzen 7 7735U with Radeon Graphics":40,
        "AMD Ryzen 5 5560U with Radeon Graphics":18,
        "AMD Ryzen 7 5700U with Radeon Graphics":28,
        "AMD Ryzen 7 5800U with Radeon Graphics":30,
        "AMD Ryzen 7 5825U with Radeon Graphics":30,
        "AMD Ryzen 7 6800U with Radeon Graphics":40,
        "AMD Ryzen 7 4800U with Radeon Graphics":25,
        "AMD Ryzen 5 4500U with Radeon Graphics":25,
        "AMD Athlon Silver 3050e with Radeon Graphics":12,
        "AMD Ryzen Z1 Extreme":40,
        "AMD Ryzen 7 7840U w/ Radeon 780M Graphics": 40,
    }
except Exception as e:
    logging.error(f"TDP配置异常|{e}")

#风扇配置
try:

    #风扇驱动配置
    FAN_HWMON_LIST={
        "oxpec":{
            "pwm_enable":"pwm1_enable",   
            "pwm":"pwm1",
            "fan_input":"fan1_input"
        },
        "asus_custom_fan_curve":{
            "manual_value": 1,
            "auto_value": 2,
            "pwm_enable_list":["pwm1_enable","pwm2_enable"],   
            "temp_first_list":["pwm1_auto_point1_temp","pwm2_auto_point1_temp"],
            "pwm_list":[
                "pwm1_auto_point1_pwm",
                "pwm1_auto_point2_pwm",
                "pwm1_auto_point3_pwm",
                "pwm1_auto_point4_pwm",
                "pwm1_auto_point5_pwm",
                "pwm1_auto_point6_pwm",
                "pwm1_auto_point7_pwm",
                "pwm1_auto_point8_pwm",
                "pwm2_auto_point1_pwm",
                "pwm2_auto_point2_pwm",
                "pwm2_auto_point3_pwm",
                "pwm2_auto_point4_pwm",
                "pwm2_auto_point5_pwm",
                "pwm2_auto_point6_pwm",
                "pwm2_auto_point7_pwm",
                "pwm2_auto_point8_pwm"
                ],
            "fan_input":"../hwmon6/fan1_input"
        },
        "steamdeck_hwmon":{
            "pwm_enable":"fan1_target",   
            "pwm":"fan1_target",
            "fan_input":"fan1_input"
        }}

    #风扇ec配置
    FAN_MANUAL_OFFSET=0     #风扇自动控制ec地址
    FAN_RPMWRITE_OFFSET=0   #风扇写入转速ec地址
    FAN_RPMREAD_OFFSET=0    #风扇读取转速ec地址
    FAN_RAM_REG_ADDR=0      #风扇ecRam寄存器地址
    FAN_RAM_REG_DATA=0      #风扇ecRam寄存器数据
    FAN_RAM_MANUAL_OFFSET=0     #风扇自动控制ecRam地址
    FAN_RAM_RPMWRITE_OFFSET=0   #风扇写入转速ecRam地址
    FAN_RAM_RPMREAD_OFFSET=0    #风扇读取转速ecRam地址
    FAN_RAM_RPMREAD_LENGTH=0    #风扇实际转速值长度 0为需要通过计算获得转速
    FAN_IS_ADAPTED=False    #风扇是否适配

    #FAN_MAXTEMP=0    #风扇图表最大温度
    #FAN_MINTEMP=0     #风扇图表最小温度
    #FAN_MAXRPM_PERCENT=0    #风扇图表最大转速百分比
    #FAN_MINRPM_PERCENT=0    #风扇图表最小转速百分比
    FAN_RPMWRITE_MAX=0      #风扇最大转速ec写入值
    FAN_RPMVALUE_MAX=0       #风扇最大转速数值
    FAN_CPUTEMP_PATH=""     #CPU温度路径
    FAN_GPUTEMP_PATH=""     #GPU温度路径
    
    if PRODUCT_NAME in (
        "ONEXPLAYER 2 ARP23",
        ):
        FAN_MANUAL_OFFSET=0x4a
        FAN_RPMWRITE_OFFSET=0x4b
        FAN_RPMREAD_OFFSET=0x58

        FAN_RAM_REG_ADDR=0x4E
        FAN_RAM_REG_DATA=0x4F
        FAN_RAM_MANUAL_OFFSET=0x44a
        FAN_RAM_RPMWRITE_OFFSET=0x44b
        FAN_RAM_RPMREAD_OFFSET=0x1809
        FAN_RAM_RPMREAD_LENGTH=0

        FAN_RPMWRITE_MAX=184
        FAN_RPMVALUE_MAX=5000
        FAN_IS_ADAPTED=True
    elif PRODUCT_NAME in (
        "AIR",
        "AIR Pro",
        ):
        FAN_MANUAL_OFFSET=0x4a
        FAN_RPMWRITE_OFFSET=0x4b
        FAN_RPMREAD_OFFSET=0x76

        FAN_RAM_REG_ADDR=0x4E
        FAN_RAM_REG_DATA=0x4F
        FAN_RAM_MANUAL_OFFSET=0x44a
        FAN_RAM_RPMWRITE_OFFSET=0x44b
        FAN_RAM_RPMREAD_OFFSET=0x1809
        FAN_RAM_RPMREAD_LENGTH=0

        FAN_RPMWRITE_MAX=255
        FAN_RPMVALUE_MAX=5811
        FAN_IS_ADAPTED=True
    elif PRODUCT_NAME in (
        "AYANEO 2",
        "AYANEO 2S",
        "GEEK",
        "GEEK 1S",
        ):
        FAN_MANUAL_OFFSET=0x4a
        FAN_RPMWRITE_OFFSET=0x4b
        FAN_RPMREAD_OFFSET=0x76

        FAN_RAM_REG_ADDR=0x4E
        FAN_RAM_REG_DATA=0x4F
        FAN_RAM_MANUAL_OFFSET=0x44a
        FAN_RAM_RPMWRITE_OFFSET=0x44b
        FAN_RAM_RPMREAD_OFFSET=0x1809
        FAN_RAM_RPMREAD_LENGTH=0

        FAN_RPMWRITE_MAX=200
        FAN_RPMVALUE_MAX=5530
        FAN_IS_ADAPTED=True
    elif PRODUCT_NAME in (
        "ONEXPLAYER Mini Pro",
        "AOKZOE A1 AR07",
        ):
        FAN_MANUAL_OFFSET=0x4a
        FAN_RPMWRITE_OFFSET=0x4b
        FAN_RPMREAD_OFFSET=0x76

        FAN_RAM_REG_ADDR=0x4E
        FAN_RAM_REG_DATA=0x4F
        FAN_RAM_MANUAL_OFFSET=0x44a
        FAN_RAM_RPMWRITE_OFFSET=0x44b
        FAN_RAM_RPMREAD_OFFSET=0x1809
        FAN_RAM_RPMREAD_LENGTH=0

        FAN_RPMWRITE_MAX=255
        FAN_RPMVALUE_MAX=4968
        FAN_IS_ADAPTED=True
    elif PRODUCT_NAME in (
        "G1618-04",
        ):
        FAN_RAM_REG_ADDR=0x2E
        FAN_RAM_REG_DATA=0x2F
        FAN_RAM_MANUAL_OFFSET=0xC311
        FAN_RAM_RPMWRITE_OFFSET=0xC311
        FAN_RAM_RPMREAD_OFFSET=0x880
        FAN_RAM_RPMREAD_LENGTH=2

        FAN_RPMWRITE_MAX=127
        FAN_RPMVALUE_MAX=4968
        FAN_IS_ADAPTED=True
    elif PRODUCT_NAME in (
        "G1619-04",
        ):
        FAN_RAM_REG_ADDR=0x4E
        FAN_RAM_REG_DATA=0x4F
        FAN_RAM_MANUAL_OFFSET=0x275
        FAN_RAM_RPMWRITE_OFFSET=0x1809
        FAN_RAM_RPMREAD_OFFSET=0x218
        FAN_RAM_RPMREAD_LENGTH=2

        FAN_RPMWRITE_MAX=184
        FAN_RPMVALUE_MAX=4968
        FAN_IS_ADAPTED=True
    elif PRODUCT_NAME in (
        "G1617-01",
        ):
        FAN_RAM_REG_ADDR=0x4E
        FAN_RAM_REG_DATA=0x4F
        FAN_RAM_MANUAL_OFFSET=0x47A
        FAN_RAM_RPMWRITE_OFFSET=0x47A
        FAN_RAM_RPMREAD_OFFSET=0x478
        FAN_RAM_RPMREAD_LENGTH=2

        FAN_RPMWRITE_MAX=244
        FAN_RPMVALUE_MAX=6500
        FAN_IS_ADAPTED=True
    elif PRODUCT_NAME in (
        "Jupiter",
        ):
        FAN_RPMWRITE_MAX=7300
        FAN_RPMVALUE_MAX=7309
        FAN_IS_ADAPTED=True
    elif PRODUCT_NAME in (
        "ROG Ally RC71L_RC71L",
        ):
        FAN_RPMWRITE_MAX=255
        FAN_RPMVALUE_MAX=8000
        FAN_IS_ADAPTED=True
except Exception as e:
    logging.error(f"风扇配置异常|{e}")
