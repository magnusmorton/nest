
import multiprocessing

def nest_fn4314459984(a):
    for i in range(2500):
        a[i] = ((2 * 3) + 45)
    return [a]
a = ([0] * 10000)
pool = multiprocessing.Pool(4)
nest_res0 = pool.apply_async(nest_fn4314459984, [a[0:2500]])
nest_res1 = pool.apply_async(nest_fn4314459984, [a[2500:5000]])
nest_res2 = pool.apply_async(nest_fn4314459984, [a[5000:7500]])
nest_res3 = pool.apply_async(nest_fn4314459984, [a[7500:10000]])
a = (((nest_res0.get()[0] + nest_res1.get()[0]) + nest_res2.get()[0]) + nest_res3.get()[0])
print(a)
