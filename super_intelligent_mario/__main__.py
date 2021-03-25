import subprocess


def main():

    proc = subprocess.Popen(["python3", "-u", "sample_reference_agents/marioRule.py"])

    while(proc):
        try:
            sig = input("type q to quit\n")
            if(sig=="q"):
                proc.kill()
                quit()
        except KeyboardInterrupt:
            proc.kill()
            quit()

if __name__ == "__main__":
    main()