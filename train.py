from Face_detect import train_v2
def main():
    for i in train_v2.train():
        yield i

if __name__=="__main__":
    main()