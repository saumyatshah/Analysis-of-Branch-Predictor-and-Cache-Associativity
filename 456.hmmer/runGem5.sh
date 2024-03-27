# --  to run SPEC 456.hmmer  --
export GEM5_DIR=/home/eng/s/sxs220366/CA/gem5
export BENCHMARK=./src/benchmark
export ARGUMENT=./data/bombesin.hmm
time $GEM5_DIR/build/X86/gem5.opt -d ./m5out $GEM5_DIR/configs/example/se.py -c $BENCHMARK -o $ARGUMENT -I 500000000 --cpu-type=atomic --caches --l2cache --l1d_size=128kB --l1i_size=128kB --l2_size=1MB --l1d_assoc=2 --l1i_assoc=2 --l2_assoc=1 --cacheline_size=64