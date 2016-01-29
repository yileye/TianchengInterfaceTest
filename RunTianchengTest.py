#coding=utf8
#######################################################
#filename:RunTianchengTest.py
#author:defias
#date:2015-11
#function: run main
#######################################################
pass

if __name__ == '__main__':
    from src import TianchengTest
    print 'RunTianchengTest Start...'
    TianchengTest.TianchengTest()
    print 'RunTianchengTest End'

    """
    from src import MockTest
    MockTest.testHttpServer2()
    """

    """
    from src import MockTest
    import multiprocessing
    import os
    print 'MockTest Start...'
    multiprocessing.freeze_support()
    print('Parent process %s.' % os.getpid())
    p = multiprocessing.Process(target=MockTest.testHttpServer)
    print('Child process will start.')
    p.start()
    print "p.pid:", p.pid
    print "p.name:", p.name
    print "p.is_alive:", p.is_alive()
    p.join()
    print('Child process end.')
    print 'MockTest End'
    """
