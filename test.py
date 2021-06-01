import lib.Discord as d
import threading

discord = d.Discord()
app = d.TDCRBot()

thread = threading.Thread(target=app.run)


def main():
    thread.start()
    #print("carry on")


if __name__ == "__main__":
    main()
