import file_util as fu
import traceback
from aiohttp import web


class Handler:
    """
    Http handler
    """
    def __init__(self):
        pass

    async def upload(self, request):
        try:
            reader = await request.multipart()
            field = await reader.next()
            assert field.name == 'name'
            helper = fu.FileHelper()
            checksum = await helper.save_file(field)
            return web.json_response({'FileHash': checksum})
        except Exception as ex:
            print('error')
            print(str(ex))
            print(traceback.format_exc())
            return web.Response(text='Internal server error', status=500)

    async def download(self, request):
        hash = request.match_info.get('hash', None)
        helper = fu.FileHelper()
        dist_file = helper.get_filepath_by_hash(hash)
        if dist_file:
            response = web.FileResponse(chunk_size=8192, path=dist_file)
            response.headers.add('filename', 'file')
            return response
        else:
            return web.Response(text='File not found', status=500)

    async def remove(self, request):
        try:
            data = await request.post()
            hash = data['hash']
            helper = fu.FileHelper()
            res = helper.remove_file_by_hash(hash)
            if res:
                return web.Response(text=res, status=500)
            return web.Response(text='File removed')
        except Exception as ex:
            print('error')
            print(str(ex))
            print(traceback.format_exc())
            return web.Response(text='Internal server error', status=500)


def run_service():
    handler = Handler()
    app = web.Application()
    app.add_routes([web.post('/upload', handler.upload),
                    web.get('/download({hash})', handler.download),
                    web.post('/remove', handler.remove)])
    web.run_app(app, port=8081)
