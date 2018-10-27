require 'ffi'

module KQueue
  # This module contains the low-level foreign-function interface code
  # for dealing with the kqueue C APIs.
  # It's an implementation detail, and not meant for users to deal with.
  #
  # @private
  module Native
    extend FFI::Library

    # The C struct describing a kqueue event.
    #
    # @private
    class KEvent < FFI::Struct
      if FFI::Platform::IS_FREEBSD
        layout(
          :ident,  :uintptr_t,
          :filter, :short,
          :flags,  :u_short,
          :fflags, :u_int,
          :data,   :intptr_t,
          :udata,  :pointer)
      elsif FFI::Platform::IS_NETBSD
        layout(
          :ident,  :uintptr_t,
          :filter, :uint32_t,
          :flags,  :uint32_t,
          :fflags, :uint32_t,
          :data,   :int64_t,
          :udata,  :pointer)
      elsif FFI::Platform::IS_OPENBSD
        layout(
          :ident,  :__uintptr_t,
          :filter, :short,
          :flags,  :u_short,
          :fflags, :u_int,
          :data,   :quad_t,
          :udata,  :pointer)
      else
        layout(
          :ident,  :uintptr_t,
          :filter, :int16,
          :flags,  :uint16,
          :fflags, :uint32,
          :data,   :intptr_t,
          :udata,  :pointer)
      end
    end

    # The C struct describing a timeout.
    #
    # @private
    class TimeSpec < FFI::Struct
      layout(
        :tv_sec, :time_t,
        :tv_nsec, :long)
    end

    ffi_lib FFI::Library::LIBC

    attach_function :kqueue, [], :int
    attach_function :kevent, [:int, :pointer, :int, :pointer, :int, :pointer], :int, :blocking => true

    attach_function :open, [:string, :int], :int
    attach_function :close, [:int], :int
  end
end
