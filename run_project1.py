import os
import subprocess
import itertools


BranchPredictor = "/home/eng/s/sxs220366/CA/gem5/src/cpu/pred/BranchPredictor.py"
BranchPredictortemp = "/home/eng/s/sxs220366/CA/CA_Project/BranchPredictortemp.py"

BaseSimpleCPU = "/home/eng/s/sxs220366/CA/gem5/src/cpu/simple/BaseSimpleCPU.py"
BaseSimpleCPUtemp = "/home/eng/s/sxs220366/CA/CA_Project/BaseSimpleCPUTemp.py"

OutputFile = "/home/eng/s/sxs220366/CA/CA_Project/output/"
ReadOutputFile = "./m5out/stats.txt"

BranchPredictorList = ['LocalBP()','BiModeBP()','TournamentBP()']
defaultValueBTB = ['2048']
defaultValueLocalBP = ['1024']
defaultValuerunBiModeBP = ['8192','8192']
defaultValuerunTournamentBP = ['1024','4096','4096']

outputStrings = ['system.cpu.branchPred.BTBMissPct','system.cpu.BranchMispredPercent']

idxBTB = 0
idxLocalPredictorSize = 1
idxGlobalPredictorSize = 2
idxChoicePredictorSize = 3

Benchmarks = ['456.hmmer','458.sjeng']

combForLocalBP = [['2048','1024','',''],['2048','2048','',''],
                  ['4096','1024','',''],['4096','2048','','']
                  ]

combForBiModeBP = [
                   ['2048','','2048','2048'],['2048','','4096','2048'],['2048','','8192','2048'],
                   ['2048','','2048','4096'],['2048','','4096','4096'],['2048','','8192','4096'],
                   ['4096','','2048','4096'],['4096','','4096','4096'],['4096','','8192','4096'],
                   ['4096','','2048','8192'],['4096','','4096','8192'],['4096','','8192','8192']
                   ]

combForTournamentBP = [
                       ['2048','1024','4096','4096'],['2048','1024','4096','8192'],
                       ['2048','2048','4096','4096'],['2048','2048','4096','8192'],
                       ['2048','2048','8192','4096'],['2048','2048','8192','8192'],
                       ['4096','1024','4096','4096'],['4096','1024','4096','8192'],
                       ['4096','2048','4096','4096'],['4096','2048','4096','8192'],
                       ['4096','2048','8192','4096'],['4096','2048','8192','8192']
                       ]

def EditBaseSimpleCPU(BranchPred):
    templateBSC = open(BaseSimpleCPUtemp , "r")
    BSCdata = templateBSC.readlines()
    templateBSC.close()

    EditBSC = open(BaseSimpleCPU, "w")

    for line in BSCdata:
        if 'BPRED' in line:
            line = line.replace('BPRED',BranchPred)
        EditBSC.write(line)
    EditBSC.close()


def runLocalBP():
    print('#################################################################')
    print('')
    print('            CHANGING PREDICTOR DATA FOR OBSERVATION              ')
    print('')
    print('#################################################################')
    for val in combForLocalBP:
       
        EditBaseSimpleCPU(BranchPredictorList[0])
        templateBP = open(BranchPredictortemp , "r")
        BPdata = templateBP.readlines()
        templateBP.close()

        EditBP = open(BranchPredictor, "w")
        
        for line in BPdata:
            if 'BTBL1' in line:
                line = line.replace('BTBL1',val[idxBTB])
            if 'LBP1' in line:
                line = line.replace('LBP1',val[idxLocalPredictorSize])
            if 'BBPL1' in line:
                line = line.replace('BBPL1',defaultValuerunBiModeBP[0])         #local
            if 'BBPL2' in line:
                line = line.replace('BBPL2',defaultValuerunBiModeBP[1])         #choice
            if 'TPL1' in line:
                line = line.replace('TPL1',defaultValuerunTournamentBP[0])      #local
            if 'TPL2' in line:
                line = line.replace('TPL2',defaultValuerunTournamentBP[1])      #global
            if 'TPL3' in line:
                line = line.replace('TPL3',defaultValuerunTournamentBP[2])      #choice

            EditBP.write(line)
        EditBP.close()
        
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
        for bm in Benchmarks:
            print('#################################################################')
            print('')
            print('                        EXECUTING '+bm+'                         ')
            print('')
            print('#################################################################')
            os.chdir(bm)
            os.system('rm -rf m5out')
            os.system('sh runGem5.sh')
            
            print('#################################################################')
            print('')
            print('CAPTURING OUTPUT OF VALUES('+val[idxBTB]  +' , ' + val[idxLocalPredictorSize] +')                          ')
            print('')
            print('#################################################################')
            readStats = open(ReadOutputFile , "r")
            Statsdata = readStats.readlines()
            readStats.close()
            
            tempbm = bm.replace('.','')
            outputFileName = OutputFile + val[idxBTB] + '_' + val[idxLocalPredictorSize] + '_LocalBP_' + tempbm +'_Output.txt'
            writeStatsData = open(outputFileName , "w")

            for line in Statsdata:
                if outputStrings[0] in line:
                    writeStatsData.write(line)
                if outputStrings[1] in line:
                    writeStatsData.write(line)
            writeStatsData.close()
            os.chdir('../')



def runBiModeBP():
    print('#################################################################')
    print('')
    print('            CHANGING PREDICTOR DATA FOR OBSERVATION              ')
    print('')
    print('#################################################################')
    for val in combForBiModeBP:
        EditBaseSimpleCPU(BranchPredictorList[1])
        templateBP = open(BranchPredictortemp , "r")
        BPdata = templateBP.readlines()
        templateBP.close()

        EditBP = open(BranchPredictor, "w")
        for line in BPdata:
            if 'BTBL1' in line:
                line = line.replace('BTBL1',val[idxBTB])
            if 'LBP1' in line:
                line = line.replace('LBP1',defaultValueLocalBP[0])
            if 'BBPL1' in line:
                line = line.replace('BBPL1',val[idxGlobalPredictorSize])         #local
            if 'BBPL2' in line:
                line = line.replace('BBPL2',val[idxChoicePredictorSize])         #choice
            if 'TPL1' in line:
                line = line.replace('TPL1',defaultValuerunTournamentBP[0])      #local
            if 'TPL2' in line:
                line = line.replace('TPL2',defaultValuerunTournamentBP[1])      #global
            if 'TPL3' in line:
                line = line.replace('TPL3',defaultValuerunTournamentBP[2])      #choice
            EditBP.write(line)
        EditBP.close()
        print('#################################################################')
        print('')
        print('                        REBUILDING GEM5                          ')
        print('')
        print('#################################################################')
        os.chdir('../gem5')
        os.system('rm -rf ./build/X86')
        os.system('scons build/X86/gem5.opt -j 4')
        os.chdir('../Project1_SPEC/')
        for bm in Benchmarks:
            print('#################################################################')
            print('')
            print('                        EXECUTING '+bm+'                         ')
            print('')
            print('#################################################################')
            os.chdir(bm)
            os.system('rm -rf m5out')
            os.system('sh runGem5.sh')
            
            print('#################################################################')
            print('')
            print('CAPTURING OUTPUT OF VALUES('+val[idxBTB]  +','+ val[idxGlobalPredictorSize] +','+ val[idxChoicePredictorSize] +')                          ')
            print('')
            print('#################################################################')
            readStats = open(ReadOutputFile , "r")
            Statsdata = readStats.readlines()
            readStats.close()
            
            tempbm = bm.replace('.','')
            outputFileName = OutputFile + val[idxBTB] + '_' + val[idxGlobalPredictorSize] + '_' + val[idxChoicePredictorSize] + '_BiModeBP_' + tempbm +'_Output.txt'
            writeStatsData = open(outputFileName , "w")

            for line in Statsdata:
                if outputStrings[0] in line:
                    writeStatsData.write(line)
                if outputStrings[1] in line:
                    writeStatsData.write(line)
            writeStatsData.close()
            os.chdir('../')

def runTournamentBP():
    print('#################################################################')
    print('')
    print('            CHANGING PREDICTOR DATA FOR OBSERVATION              ')
    print('')
    print('#################################################################')
    for val in combForTournamentBP:
        EditBaseSimpleCPU(BranchPredictorList[2])
        templateBP = open(BranchPredictortemp , "r")
        BPdata = templateBP.readlines()
        templateBP.close()

        EditBP = open(BranchPredictor, "w")
        for line in BPdata:
            if 'BTBL1' in line:
                line = line.replace('BTBL1',val[idxBTB])
            if 'LBP1' in line:
                line = line.replace('LBP1',defaultValueLocalBP[0])
            if 'BBPL1' in line:
                line = line.replace('BBPL1',defaultValuerunBiModeBP[0])         #local
            if 'BBPL2' in line:
                line = line.replace('BBPL2',defaultValuerunBiModeBP[1])         #choice
            if 'TPL1' in line:
                line = line.replace('TPL1',val[idxLocalPredictorSize])      #local
            if 'TPL2' in line:
                line = line.replace('TPL2',val[idxGlobalPredictorSize])      #global
            if 'TPL3' in line:
                line = line.replace('TPL3',val[idxChoicePredictorSize])      #choice
            EditBP.write(line)
        EditBP.close()
        print('#################################################################')
        print('')
        print('                        REBUILDING GEM5                          ')
        print('')
        print('#################################################################')
        os.chdir('../gem5')
        os.system('rm -rf ./build/X86')
        os.system('scons build/X86/gem5.opt -j 4')
        os.chdir('../Project1_SPEC/')
        for bm in Benchmarks:
            print('#################################################################')
            print('')
            print('                        EXECUTING '+bm+'                         ')
            print('')
            print('#################################################################')
            os.chdir(bm)
            os.system('rm -rf m5out')
            os.system('sh runGem5.sh')
            
            print('#################################################################')
            print('')
            print('CAPTURING OUTPUT OF VALUES('+val[idxBTB] + val[idxLocalPredictorSize] + val[idxGlobalPredictorSize] + val[idxChoicePredictorSize] +')                          ')
            print('')
            print('#################################################################')
            readStats = open(ReadOutputFile , "r")
            Statsdata = readStats.readlines()
            readStats.close()
            
            tempbm = bm.replace('.','')
            outputFileName = OutputFile + val[idxBTB] + '_' + val[idxLocalPredictorSize] +'_'+val[idxGlobalPredictorSize] + '_' + val[idxChoicePredictorSize] + '_TournamentBP_' + tempbm +'_Output.txt'
            writeStatsData = open(outputFileName , "w")

            for line in Statsdata:
                if outputStrings[0] in line:
                    writeStatsData.write(line)
                if outputStrings[1] in line:
                    writeStatsData.write(line)
            writeStatsData.close()
            os.chdir('../')

if __name__=="__main__":
    runLocalBP()
    runBiModeBP()
    runTournamentBP()
