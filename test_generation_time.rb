require 'gnuplot'

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


puts "running simple generation time benchmarks"
simple_times = []
100.times do 
  time = Time.now.to_f
  `nest test_files/simple_multidim.py`
  simple_times << (Time.now.to_f - time)
end

puts simple_times
simple_avg = simple_times.mean
  p "AVG: #{simple_avg}"
puts simple_times.standard_deviation

puts "running complex generation time benchmarks"
complex_times = []
100.times do
  time = Time.now.to_f
  `nest test_files/complex.py`
  complex_times << (Time.now.to_f - time)
end

puts complex_times
complex_avg = complex_times.mean
puts "stddev: #{complex_times.standard_deviation}"
  p "AVG: #{complex_avg}"
puts "running even more complex generation time benchmarks"
long_complex_times = []
100.times do
  time = Time.now.to_f
  `nest test_files/long_complex.py`
  long_complex_times << (Time.now.to_f - time)
end

puts long_complex_times

long_avg = long_complex_times.mean
puts "stddev: #{long_complex_times.standard_deviation}"
  p "AVG: #{long_avg}"
## word counts

simple_lines = `wc -l test_files/simple.py`.match(/(\d+)/)[0]
complex_lines = `wc -l test_files/complex.py`.match(/(\d+)/)[0]
long_lines = `wc -l test_files/long_complex.py`.match(/(\d+)/)[0]


Gnuplot.open do |gp|
  Gnuplot::Plot.new(gp) do |plot|
      plot.title "Generation time against line count"
      plot.terminal "png"
      plot.output File.expand_path("timevslines.png")
      x = [simple_lines, complex_lines, long_lines]
      y = [simple_avg, complex_avg, long_avg]
      plot.data << Gnuplot::DataSet.new([x,y]) do |ds|
        ds.with = "lines"
        ds.linewidth = 4
      end
    end
  end
      
