import utils_fun
import pandas as pd
import globals_var
import cherrypy
import os


# def find_top_images(text, k=5):
#     result = utils.sub_string_matching(text, threshold=0.6)



# matched_images = get_top_images("i want to see a cat")
# print("matched_images: : ", matched_images)

server_config = {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8071,
        'tools.cors.on':      True
}

class Api:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def query_images(self, query, k=5):
        #data = cherrypy.request.json
        #print("data : ", data)
        return utils_fun.get_top_images(query, int(k))
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def serve_image(self, image):
        print("Here :::::")
        image = os.path.abspath(image)
        print("image: ", image)
        return cherrypy.lib.static.serve_file(image)

    @cherrypy.expose
    # @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def add_record(self, image_raw, description, category):
        # Now we have uploaded image
        # image = utils_fun.upload_image(image_raw, globals_var.IMAGE_FOLDER_PATH)
        image = utils_fun.upload_image(image_raw, globals_var.IMAGE_FOLDER_PATH)
        # Now we have to add entry in database
        # AND refresh the database code to load all text again
        globals_var.images.append(image)
        globals_var.texts.append(description.strip())
        # Now add in databse
        globals_var.db.images_data.insert({
            "image_path": image,
            "text": description.strip(),
            "category": category
        })

        return {"code": 1, "message": "Successfully added"}
def cors():
    if cherrypy.request.method == 'OPTIONS':
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
        cherrypy.response.headers[
            'Access-Control-Allow-Headers'] = 'content-type'
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return True
    else:
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'


# In[10]:


if __name__ == '__main__':
    # noinspection PyProtectedMember
    cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)
    cherrypy.config.update(server_config)
    cherrypy.response.timeout = 1000000000
    api = Api()
    cherrypy.quickstart(api)
