protoc -I=. timeseries.proto \
--js_out=import_style=commonjs:generated \
--grpc-web_out=import_style=commonjs,mode=grpcwebtext:generated
