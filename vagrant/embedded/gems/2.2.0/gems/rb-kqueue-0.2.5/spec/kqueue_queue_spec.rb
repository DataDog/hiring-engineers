require_relative '../lib/rb-kqueue'
require 'tempfile'
require 'pathname'

RSpec.describe KQueue::Queue do
  describe '#watch_file' do
    let(:file_touched) { false }
    let(:queue) { KQueue::Queue.new }
    let(:file) { Tempfile.new 'rb-kqueue_test', Pathname(__dir__).parent.join('tmp') }

    context 'file is watched for writes' do
      before do
	queue.watch_file file.path, :write do
	  file_touched = !file_touched
	end
	queue.process
      end

      context 'file is written to' do
	it 'executes the defined block' do
	  expect { file.write 'test' }.to change { file_touched }.from(false).to true
	end
      end
    end

    context 'file is watched for reads' do
    end

    context 'file is not watched' do
    end
  end
end
