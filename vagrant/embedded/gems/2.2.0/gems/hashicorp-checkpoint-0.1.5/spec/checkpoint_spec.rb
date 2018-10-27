require "tempfile"

require "helper"

describe Checkpoint do
  describe ".check" do
    before do
      allow(ENV).to receive(:[]).and_return(nil)
    end

    context "with a proper request" do
      subject do
        described_class.check(
          product: "test",
          version: "1.0",
          raise_error: true,
        )
      end

      its(["alerts"]) { should be_empty }
      its(["current_version"]) { should eq("1.0") }
      its(["outdated"]) { should eq(false) }
      its(["product"]) { should eq("test") }
    end

    context "cache file" do
      let(:path){ @path }

      before do
        tf = Tempfile.new("checkpoint")
        tfpath = tf.path
        tf.close
        File.unlink(tfpath)
        @path = tfpath
      end

      after{ File.unlink(path) if File.exist?(path) }

      it "should cache things with cache_file" do
        opts = {
          product: "test",
          version: "1.0",
          cache_file: path,
        }

        # Just run it twice
        c = described_class.check(opts)
        c = described_class.check(opts)

        expect(c["product"]).to eq("test")
      end

      it "should indicate cached result" do
        opts = {
          product: "test",
          version: "1.0",
          cache_file: path,
        }

        # Just run it twice
        c = described_class.check(opts)
        c = described_class.check(opts)

        expect(c["cached"]).to eq(true)
      end
    end

    context "with errors" do
      let(:error_class){ StandardError }
      let(:opts) {
        {
          product: "test",
          version: "1.0"
        }
      }
      before{ allow(Net::HTTP).to receive(:new).and_raise(error_class) }

      it "should not raise error by default" do
        expect(described_class.check(opts)).to be_nil
      end

      it "should raise error when option set" do
        expect{ described_class.check(opts.merge(raise_error: true)) }.to raise_error(error_class)
      end

      context "with non-StandardError descendant exception" do
        let(:error_class){ Interrupt }

        it "should raise error by default" do
          expect{ described_class.check(opts) }.to raise_error(error_class)
        end

        it "should raise error when option set" do
          expect{ described_class.check(opts.merge(raise_error: true)) }.to raise_error(error_class)
        end
      end
    end

    it "does not check when CHECKPOINT_DISABLE=1" do
      allow(ENV).to receive(:[])
        .with("CHECKPOINT_DISABLE")
        .and_return(1)
      expect(described_class.check).to be(nil)
    end
  end
end
