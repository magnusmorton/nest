puts "running simple generation time benchmarks"
simple_times = []
100.times do 
  time = Time.now.to_f
  `nest test_files/simple_multidim.py`
  simple_times << (Time.now.to_f - time)
end

puts simple_times

puts "running complex generation time benchmarks"
complex_times = []
100.times do
  time = Time.now.to_f
  `nest test_files/complex.py`
  complex_times << (Time.now.to_f - time)
end

puts complex_times

puts "running even more complex generation time benchmarks"
long_complex_times = []
100.times do
  time = Time.now.to_f
  `nest test_files/long_complex.py`
  long_complex_times << (Time.now.to_f - time)
end

puts long_complex_times
