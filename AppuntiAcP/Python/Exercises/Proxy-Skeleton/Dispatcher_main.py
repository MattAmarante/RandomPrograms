from Dispatcher import Dispatcher,Skeleton

IP = 'localhost'
PORT = 5000

if __name__ == "__main__":
    DispatcherClass = Dispatcher()
    SkeletonClass = Skeleton(ip = IP, port = PORT, Disp = DispatcherClass)

    SkeletonClass.runSkeleton()
    