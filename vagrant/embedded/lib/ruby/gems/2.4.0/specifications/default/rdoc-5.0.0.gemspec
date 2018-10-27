# -*- encoding: utf-8 -*-
# stub: rdoc 5.0.0 ruby lib

Gem::Specification.new do |s|
  s.name = "rdoc".freeze
  s.version = "5.0.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 2.2".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Eric Hodel".freeze, "Dave Thomas".freeze, "Phil Hagelberg".freeze, "Tony Strauss".freeze, "Zachary Scott".freeze, "Hiroshi SHIBATA".freeze]
  s.bindir = "exe".freeze
  s.date = "2018-08-28"
  s.description = "RDoc produces HTML and command-line documentation for Ruby projects.\nRDoc includes the +rdoc+ and +ri+ tools for generating and displaying documentation from the command-line.\n".freeze
  s.email = ["drbrain@segment7.net".freeze, "".freeze, "".freeze, "".freeze, "mail@zzak.io".freeze, "hsbt@ruby-lang.org".freeze]
  s.executables = ["rdoc".freeze, "ri".freeze]
  s.extra_rdoc_files = ["CVE-2013-0256.rdoc".freeze, "CONTRIBUTING.rdoc".freeze, "ExampleMarkdown.md".freeze, "ExampleRDoc.rdoc".freeze, "History.rdoc".freeze, "LEGAL.rdoc".freeze, "LICENSE.rdoc".freeze, "README.rdoc".freeze, "RI.rdoc".freeze, "TODO.rdoc".freeze]
  s.files = ["CONTRIBUTING.rdoc".freeze, "CVE-2013-0256.rdoc".freeze, "ExampleMarkdown.md".freeze, "ExampleRDoc.rdoc".freeze, "History.rdoc".freeze, "LEGAL.rdoc".freeze, "LICENSE.rdoc".freeze, "README.rdoc".freeze, "RI.rdoc".freeze, "TODO.rdoc".freeze, "exe/rdoc".freeze, "exe/ri".freeze, "rdoc.rb".freeze, "rdoc/alias.rb".freeze, "rdoc/anon_class.rb".freeze, "rdoc/any_method.rb".freeze, "rdoc/attr.rb".freeze, "rdoc/class_module.rb".freeze, "rdoc/code_object.rb".freeze, "rdoc/code_objects.rb".freeze, "rdoc/comment.rb".freeze, "rdoc/constant.rb".freeze, "rdoc/context.rb".freeze, "rdoc/context/section.rb".freeze, "rdoc/cross_reference.rb".freeze, "rdoc/encoding.rb".freeze, "rdoc/erb_partial.rb".freeze, "rdoc/erbio.rb".freeze, "rdoc/extend.rb".freeze, "rdoc/generator.rb".freeze, "rdoc/generator/darkfish.rb".freeze, "rdoc/generator/json_index.rb".freeze, "rdoc/generator/markup.rb".freeze, "rdoc/generator/pot.rb".freeze, "rdoc/generator/pot/message_extractor.rb".freeze, "rdoc/generator/pot/po.rb".freeze, "rdoc/generator/pot/po_entry.rb".freeze, "rdoc/generator/ri.rb".freeze, "rdoc/ghost_method.rb".freeze, "rdoc/i18n.rb".freeze, "rdoc/i18n/locale.rb".freeze, "rdoc/i18n/text.rb".freeze, "rdoc/include.rb".freeze, "rdoc/known_classes.rb".freeze, "rdoc/markdown.rb".freeze, "rdoc/markdown/entities.rb".freeze, "rdoc/markdown/literals.rb".freeze, "rdoc/markup.rb".freeze, "rdoc/markup/attr_changer.rb".freeze, "rdoc/markup/attr_span.rb".freeze, "rdoc/markup/attribute_manager.rb".freeze, "rdoc/markup/attributes.rb".freeze, "rdoc/markup/blank_line.rb".freeze, "rdoc/markup/block_quote.rb".freeze, "rdoc/markup/document.rb".freeze, "rdoc/markup/formatter.rb".freeze, "rdoc/markup/formatter_test_case.rb".freeze, "rdoc/markup/hard_break.rb".freeze, "rdoc/markup/heading.rb".freeze, "rdoc/markup/include.rb".freeze, "rdoc/markup/indented_paragraph.rb".freeze, "rdoc/markup/inline.rb".freeze, "rdoc/markup/list.rb".freeze, "rdoc/markup/list_item.rb".freeze, "rdoc/markup/paragraph.rb".freeze, "rdoc/markup/parser.rb".freeze, "rdoc/markup/pre_process.rb".freeze, "rdoc/markup/raw.rb".freeze, "rdoc/markup/rule.rb".freeze, "rdoc/markup/special.rb".freeze, "rdoc/markup/text_formatter_test_case.rb".freeze, "rdoc/markup/to_ansi.rb".freeze, "rdoc/markup/to_bs.rb".freeze, "rdoc/markup/to_html.rb".freeze, "rdoc/markup/to_html_crossref.rb".freeze, "rdoc/markup/to_html_snippet.rb".freeze, "rdoc/markup/to_joined_paragraph.rb".freeze, "rdoc/markup/to_label.rb".freeze, "rdoc/markup/to_markdown.rb".freeze, "rdoc/markup/to_rdoc.rb".freeze, "rdoc/markup/to_table_of_contents.rb".freeze, "rdoc/markup/to_test.rb".freeze, "rdoc/markup/to_tt_only.rb".freeze, "rdoc/markup/verbatim.rb".freeze, "rdoc/meta_method.rb".freeze, "rdoc/method_attr.rb".freeze, "rdoc/mixin.rb".freeze, "rdoc/normal_class.rb".freeze, "rdoc/normal_module.rb".freeze, "rdoc/options.rb".freeze, "rdoc/parser.rb".freeze, "rdoc/parser/c.rb".freeze, "rdoc/parser/changelog.rb".freeze, "rdoc/parser/markdown.rb".freeze, "rdoc/parser/rd.rb".freeze, "rdoc/parser/ruby.rb".freeze, "rdoc/parser/ruby_tools.rb".freeze, "rdoc/parser/simple.rb".freeze, "rdoc/parser/text.rb".freeze, "rdoc/rd.rb".freeze, "rdoc/rd/block_parser.rb".freeze, "rdoc/rd/inline.rb".freeze, "rdoc/rd/inline_parser.rb".freeze, "rdoc/rdoc.rb".freeze, "rdoc/require.rb".freeze, "rdoc/ri.rb".freeze, "rdoc/ri/driver.rb".freeze, "rdoc/ri/formatter.rb".freeze, "rdoc/ri/paths.rb".freeze, "rdoc/ri/store.rb".freeze, "rdoc/ri/task.rb".freeze, "rdoc/ruby_lex.rb".freeze, "rdoc/ruby_token.rb".freeze, "rdoc/rubygems_hook.rb".freeze, "rdoc/servlet.rb".freeze, "rdoc/single_class.rb".freeze, "rdoc/stats.rb".freeze, "rdoc/stats/normal.rb".freeze, "rdoc/stats/quiet.rb".freeze, "rdoc/stats/verbose.rb".freeze, "rdoc/store.rb".freeze, "rdoc/task.rb".freeze, "rdoc/test_case.rb".freeze, "rdoc/text.rb".freeze, "rdoc/token_stream.rb".freeze, "rdoc/tom_doc.rb".freeze, "rdoc/top_level.rb".freeze]
  s.homepage = "https://rdoc.github.io/rdoc".freeze
  s.licenses = ["Ruby".freeze]
  s.rdoc_options = ["--main".freeze, "README.rdoc".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 1.9.3".freeze)
  s.rubygems_version = "2.6.14.1".freeze
  s.summary = "RDoc produces HTML and command-line documentation for Ruby projects".freeze

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<rake>.freeze, [">= 0"])
      s.add_development_dependency(%q<racc>.freeze, ["> 1.4.10"])
      s.add_development_dependency(%q<kpeg>.freeze, [">= 0"])
      s.add_development_dependency(%q<minitest>.freeze, ["~> 4"])
    else
      s.add_dependency(%q<rake>.freeze, [">= 0"])
      s.add_dependency(%q<racc>.freeze, ["> 1.4.10"])
      s.add_dependency(%q<kpeg>.freeze, [">= 0"])
      s.add_dependency(%q<minitest>.freeze, ["~> 4"])
    end
  else
    s.add_dependency(%q<rake>.freeze, [">= 0"])
    s.add_dependency(%q<racc>.freeze, ["> 1.4.10"])
    s.add_dependency(%q<kpeg>.freeze, [">= 0"])
    s.add_dependency(%q<minitest>.freeze, ["~> 4"])
  end
end
