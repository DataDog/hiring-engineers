require "sinatra"
require "pg"
require "active_record"
require 'statsd'

ActiveRecord::Base.establish_connection({
  adapter: 'postgresql',
  database: 'photo_galleries'
})

class Gallery < ActiveRecord::Base
  has_many :images
end

class Image < ActiveRecord::Base
end

statsd = Statsd.new('localhost', 8125)

get "/" do
  start_time = Time.now
  @galleries = Gallery.all
  duration = Time.now - start_time
  
  statsd.histogram('pixtr.pages.response.time', duration, tags: ['support', "page:home"])
  statsd.increment('pixtr.pages.views', tags: ['support', "page:home"])

  erb :index
end 

post "/galleries" do
  gallery = Gallery.create(params[:gallery])
  redirect "/galleries/#{gallery.id}"
end

get "/galleries/new" do
  erb :new_gallery
end

get "/galleries/:id" do
  start_time = Time.now
  @gallery = Gallery.find(params[:id])
  @images = @gallery.images
  duration = Time.now - start_time

  statsd.histogram("pixtr.pages.response.time", duration, tags: ['support', "page:gallery#{@gallery.name}"])
  statsd.increment("pixtr.pages.views", tags: ['support', "page:gallery#{@gallery.name}"])

  erb :gallery
end 

get "/galleries/:id/edit" do
  @gallery = Gallery.find(params[:id])
  erb :edit_gallery
end

patch "/galleries/:id" do
  gallery = Gallery.find(params[:id])
  gallery.update(params[:gallery])
  redirect "/galleries/#{gallery.id}"
end

delete "/galleries/:id" do
  gallery = Gallery.find(params[:id])
  gallery.destroy
  redirect "/"
end

get "/galleries/:gallery_id/images/new" do
  @gallery = Gallery.find(params[:gallery_id])
  erb :new_image
end

post "/galleries/:gallery_id/images" do 
  gallery = Gallery.find(params[:gallery_id])
  gallery.images.create(params[:image])
  redirect "/galleries/#{gallery.id}"
end

get "/galleries/:gallery_id/images/:id/edit" do
  @gallery = Gallery.find(params[:gallery_id])
  @image = @gallery.images.find(params[:id])
  erb :edit_image
end

patch "/galleries/:gallery_id/images/:id" do
  gallery = Gallery.find(params[:gallery_id])
  image = gallery.images.find(params[:id])
  image.update(params[:image])
  redirect "/galleries/#{gallery.id}"
end

delete "/galleries/:gallery_id/images/:id" do
  gallery = Gallery.find(params[:gallery_id])
  image = gallery.images.find(params[:id])
  image.destroy
  redirect "/galleries/#{gallery.id}"
end
