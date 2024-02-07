import os
import itertools

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


RunGem5 = "./runGem5.sh"
RunGem5temp = "/home/eng/s/sxs220366/CA/CA_Project/runGem5Temp.sh"

PATH="/home/eng/s/sxs220366/CA/gem5"

OutputFile = "/home/eng/s/sxs220366/CA/CA_Project/output_project2/"
ReadOutputFile = "./m5out/stats.txt"

outputStrings = ['system.cpu.dcache.overall_miss_rate::total','system.cpu.icache.overall_miss_rate::total','system.l2.overall_miss_rate::total',
                 'system.l2.overall_misses::total','system.cpu.icache.overall_misses::total','system.cpu.dcache.overall_misses::total']

instructions = "50000000"
cputype = "TimingSimpleCPU"
CacheSize = ['64','128']
BlockSize = ['256','512']
Asso = ['1','4','8']


Benchmarks_456hmmer = 0
Benchmarks_458sjeng = 1
Benchmarks = ['456.hmmer','458.sjeng']
ArgFiles = ['bombesin.hmm','test.txt']

def EditRunGem5(BM,L1DSIZE,L1ISIZE,L2SIZE,L1DASSOC,L2ASSOC,L1DISSOC,BLOCKSIZE):
    templateRG5 = open(RunGem5temp , "r")
    RG5data = templateRG5.readlines()
    templateRG5.close()

    EditRG5 = open(RunGem5, "w")

    for line in RG5data:
        if 'ARGFILENAME' in line:
            line = line.replace('ARGFILENAME',ArgFiles[BM])
        if 'PATH' in line:
            line = line.replace('PATH',PATH)
        if 'CPUTYPE' in line:
            line = line.replace('CPUTYPE',cputype)
        if 'INSTRUCTIONS' in line:
            line = line.replace('INSTRUCTIONS',instructions)
        if 'L1DSIZE' in line:
            line = line.replace('L1DSIZE',L1DSIZE+'kB')
        if 'L1ISIZE' in line:
            line = line.replace('L1ISIZE',L1ISIZE+'kB')
        if 'L2SIZE' in line:
            line = line.replace('L2SIZE',L2SIZE+'MB') 
        if 'L1DASSOC' in line:
            line = line.replace('L1DASSOC',L1DASSOC)
        if 'L1DISSOC' in line:
            line = line.replace('L1DISSOC',L1DISSOC)
        if 'L2ASSOC' in line:
            line = line.replace('L2ASSOC',L2ASSOC)
        if 'BLOCKSIZE' in line:
            line = line.replace('BLOCKSIZE',BLOCKSIZE)
        EditRG5.write(line)
    EditRG5.close()


def RunrunGem5(bm):
        print('#################################################################')
        print('')
        print('                        REBUILDING GEM5                          ')
        print('')
        print('#################################################################')
        #run cmd
        os.chdir('../gem5')
        os.system('rm -rf ./build/X86')
        os.system('scons build/X86/gem5.opt -j 4')
        os.chdir('../Project1_SPEC/')
        bechCount = 1
        os.chdir(Benchmarks[bm])
        for ld2, l1, l2a, l1a, blk in itertools.product(CacheSize, CacheSize, Asso, Asso, BlockSize):
            EditRunGem5(bm,ld2,ld2,l1,l2a,l2a,l1a,blk)
            print('#################################################################')
            print('')
            print('                        EXECUTING '+Benchmarks[bm]+'                         ')
            print('')
            print(bcolors.OKGREEN+ld2+'kB_'+ld2+'kB_'+l1+'MB_'+l2a+'_'+l2a+'_'+l1a+'_'+blk+"  bechCount: " + str(bechCount) +  bcolors.ENDC)
            print('')
            print('#################################################################')
            os.system('rm -rf m5out')
            if 0 != os.system('sh runGem5.sh'):
                  print(bcolors.FAIL+ld2+'kB_'+ld2+'kB_'+l1+'MB_'+l2a+'_'+l2a+'_'+l1a+'_'+blk+ bcolors.ENDC)
                  return;

            readStats = open(ReadOutputFile , "r")
            Statsdata = readStats.readlines()
            readStats.close()
            
            tempbm = Benchmarks[bm].replace('.','')
            tempbm = OutputFile + tempbm + "_output.txt"
            writeStatsData = open(tempbm , "a")
            writeStatsData.write(ld2+'kB_'+ld2+'kB_'+l1+'MB_'+l2a+'_'+l2a+'_'+l1a+'_'+blk +"  bechCount: " + str(bechCount) )
            writeStatsData.write("\n------------------------------------------------------------------------------------------------------------------------------\n")
            for line in Statsdata:
                if outputStrings[0] in line:
                    writeStatsData.write(line)
                if outputStrings[1] in line:
                    writeStatsData.write(line)
                if outputStrings[2] in line:
                    writeStatsData.write(line)
                if outputStrings[3] in line:
                    writeStatsData.write(line)
                if outputStrings[4] in line:
                    writeStatsData.write(line)
                if outputStrings[5] in line:
                    writeStatsData.write(line)
            writeStatsData.write("#################################################################################################################################\n\n")
            writeStatsData.close()
            bechCount = bechCount + 1
        os.chdir('../CA_Project/')


if __name__=="__main__":
    RunrunGem5(Benchmarks_456hmmer)
    RunrunGem5(Benchmarks_458sjeng)
