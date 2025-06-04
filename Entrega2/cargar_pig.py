# -*- coding: utf-8 -*-

import subprocess
import os
import time

PIG_SCRIPT = "/scripts/filtrar.pig"
OUTPUT_DIR = "/scripts/resultados"
LOCAL_DIR = os.getcwd()


def run_pig_script():
    cmd = ["pig", "-x", "local", PIG_SCRIPT]
    print("Ejecutando script Pig")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    print(stdout)
    if proc.returncode != 0:
        print("Error al ejecutar pig:")
        print(stderr)
        return False
    return True

def main():
    run_pig_script()

if __name__ == "__main__":
    main()