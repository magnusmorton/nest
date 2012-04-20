
	
# from http://stackoverflow.com/questions/7749568/how-can-i-do-standard-deviation-in-ruby
module Enumerable

    def sum
      self.inject(0){|accum, i| accum + i }
    end

    def mean
      self.sum/self.length.to_f
    end

    def sample_variance
      m = self.mean
      sum = self.inject(0){|accum, i| accum +(i-m)**2 }
      sum/(self.length - 1).to_f
    end

    def standard_deviation
      return Math.sqrt(self.sample_variance)
    end

end 

puts "benchmarking simple loop, multidimensional"

simple_multidim = []
100.times do
  time = Time.now.to_f
  `python test_files/simple_multidim.py`
  simple_multidim << (Time.now.to_f - time)
end

puts simple_multidim

puts "mean: #{simple_multidim.mean}"
puts "stdev: #{simple_multidim.standard_deviation}"

File.open('simple_multidim.txt', 'w') do |f|
  simple_multidim.each do |elm|
    f.puts elm
  end
  f.puts "mean: #{simple_multidim.mean}"
  f.puts "stdev: #{simple_multidim.standard_deviation}"
end

puts "generating parallel code"
`nest test_files/simple_multidim.py`

p "running parallel code"
parallel_multidim = []
100.times do
  time = Time.now.to_f
  `python output.py`
  parallel_multidim << (Time.now.to_f - time)
end

puts parallel_multidim
puts "mean: #{parallel_multidim.mean}"
puts "stdev: #{parallel_multidim.standard_deviation}"
File.open('parallel_multidim.txt', 'w') do |f|
  parallel_multidim.each do |elm|
    f.puts elm
  end
  f.puts "mean: #{parallel_multidim.mean}"
  f.puts "stdev: #{parallel_multidim.standard_deviation}"
end

puts "benchmarking complex loop"

complex = []
100.times do
  time = Time.now.to_f
  `python test_files/complex.py`
  complex << (Time.now.to_f - time)
end

puts complex

puts "mean: #{complex.mean}"
puts "stdev: #{complex.standard_deviation}"

File.open('complex.txt', 'w') do |f|
  complex.each do |elm|
    f.puts elm
  end
  f.puts "mean: #{complex.mean}"
  f.puts "stdev: #{complex.standard_deviation}"
end

puts "generating parallel complexcode"
`nest test_files/complex.py`

p "running parallel complexcode"
parallel_multidim = []
100.times do
  time = Time.now.to_f
  `python output.py`
  parallel_multidim << (Time.now.to_f - time)
end

puts parallel_multidim
puts "mean: #{parallel_multidim.mean}"
puts "stdev: #{parallel_multidim.standard_deviation}"
File.open('parallel_complex.txt', 'w') do |f|
  parallel_multidim.each do |elm|
    f.puts elm
  end
  f.puts "mean: #{parallel_multidim.mean}"
  f.puts "stdev: #{parallel_multidim.standard_deviation}"
end

puts "benchmarking simple loop"

complex = []
100.times do
  time = Time.now.to_f
  `python test_files/simple.py`
  complex << (Time.now.to_f - time)
end

puts complex

puts "mean: #{complex.mean}"
puts "stdev: #{complex.standard_deviation}"

File.open('simple.txt', 'w') do |f|
  complex.each do |elm|
    f.puts elm
  end
  f.puts "mean: #{complex.mean}"
  f.puts "stdev: #{complex.standard_deviation}"
end

puts "generating parallel simple loop"
`nest test_files/simple.py`

p "running parallel simple loop"
parallel_multidim = []
100.times do
  time = Time.now.to_f
  `python output.py`
  parallel_multidim << (Time.now.to_f - time)
end

puts parallel_multidim
puts "mean: #{parallel_multidim.mean}"
puts "stdev: #{parallel_multidim.standard_deviation}"
File.open('parallel_simple.txt', 'w') do |f|
  parallel_multidim.each do |elm|
    f.puts elm
  end
  f.puts "mean: #{parallel_multidim.mean}"
  f.puts "stdev: #{parallel_multidim.standard_deviation}"
end
