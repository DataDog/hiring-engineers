module RubyDep
  class Warning
    PREFIX = 'RubyDep: WARNING: '.freeze
    MSG_BUGGY = 'Your Ruby is outdated/buggy.'.freeze
    MSG_INSECURE = 'Your Ruby has security vulnerabilities!'.freeze

    MSG_HOW_TO_DISABLE = ' (To disable warnings, set'\
      ' RUBY_DEP_GEM_SILENCE_WARNINGS=1)'.freeze

    OPEN_ISSUE_FOR_UNRECOGNIZED = 'If this version is important,'\
      ' please open an issue at http://github.com/e2/ruby_dep'.freeze

    def show_warnings
      return if silenced?
      case (status = check_ruby)
      when :insecure
        warn_ruby(MSG_INSECURE, status)
      when :buggy
        warn_ruby(MSG_BUGGY, status)
      when :unknown
      else
        raise "Unknown problem type: #{problem.inspect}"
      end
    end

    private

    VERSION_INFO = {
      'ruby' => {
        '2.3.1' => :unknown,
        '2.3.0' => :buggy,
        '2.2.5' => :unknown,
        '2.2.4' => :buggy,
        '2.2.0' => :insecure,
        '2.1.9' => :buggy,
        '2.0.0' => :insecure
      },

      'jruby' => {
        '2.2.3' => :unknown, # jruby-9.0.5.0
        '2.2.0' => :insecure
      }
    }.freeze

    def check_ruby
      version = Gem::Version.new(RUBY_VERSION)
      current_ruby_info.each do |ruby, status|
        return status if version >= Gem::Version.new(ruby)
      end
      :insecure
    end

    def silenced?
      value = ENV['RUBY_DEP_GEM_SILENCE_WARNINGS']
      (value || '0') !~ /^0|false|no|n$/
    end

    def warn_ruby(msg, status)
      STDERR.puts PREFIX + msg + MSG_HOW_TO_DISABLE
      STDERR.puts PREFIX + recommendation(status)
    end

    def recommendation(status)
      msg = "Your Ruby is: #{RUBY_VERSION}"
      return msg + recommendation_for_unknown unless recognized?

      msg += " (#{status})."
      msg += " Recommendation: install #{recommended(:unknown).join(' or ')}."
      return msg unless status == :insecure

      msg + " (Or, at least to #{recommended(:buggy).join(' or ')})"
    end

    def recommended(status)
      current = Gem::Version.new(RUBY_VERSION)
      current_ruby_info.select do |key, value|
        value == status && Gem::Version.new(key) > current
      end.keys.reverse
    end

    def current_ruby_info
      VERSION_INFO[RUBY_ENGINE] || {}
    end

    def recognized?
      current_ruby_info.any?
    end

    def recommendation_for_unknown
      format(
        " '%s' (unrecognized). %s", RUBY_ENGINE,
        OPEN_ISSUE_FOR_UNRECOGNIZED
      )
    end
  end
end
