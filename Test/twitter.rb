require "optparse"
require "json"
require "twitter"

# Parse the command line args
opts = {}
OptionParser.new do |opt|
  opt.on("-d", "--delay DELAY", "The delay in seconds before each tweet") do |o|
    opts[:delay] = o
  end
  opt.on("-c", "--content CONTENT", "JSON file path (contains array of tweets and token)") do |o|
    opts[:content] = o
  end
end.parse!

# Error if either of the args are missing
unless opts[:delay] && opts[:content]
  $stderr.puts "Error: you must specify both the --delay and --content options."
  exit 1
end

# Parse the content JSON file
content_file = File.read(opts[:content])
content = JSON.parse(content_file)

# Configure the Twitter client
client = Twitter::REST::Client.new do |config|
  config.consumer_key = content["config"]["consumer_key"]
  config.consumer_secret = content["config"]["consumer_secret"]
  config.access_token = content["config"]["access_token"]
  config.access_token_secret = content["config"]["access_token_secret"]
end

# Tweet each tweet with a delay
content["tweets"].each do |tweet|
  sleep opts[:delay].to_i
  client.update(tweet)
end