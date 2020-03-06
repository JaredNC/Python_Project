import newciv_bot as nc
import battle as bat
import sys

print(sys.argv)
print(f"Test: {sys.argv[1]} Test2: {sys.argv[2]}")

a = min(int(sys.argv[1]), 5000)
b = min(int(sys.argv[2]), 5000)
a = 0 if a == b else a


try:
    new_b = bat.BattleBB(a, b)
    test, winner = new_b.battle_bb()
    new = nc.NewcivLogin()
    new_p = new.make_newpost(test, 1054931)
    print(f"Success! Winner: {winner}")
except:
    print(f"Failure! a: {a} b: {b}")
