from time import sleep

import docker

client = docker.from_env()


def build_image(dockerfile_path, dockerfile_name, image_tag):
    try:
        print("build executed")
        client.images.build(path=dockerfile_path, dockerfile=dockerfile_name, tag=image_tag, forcerm=True)
        return True
    except Exception as err:
        print(err)
        return False


def force_installation_dockers(image_tag_list):
    for image_dict in image_tag_list:
        if image_dict["image_tag"]:
            print(image_dict["image_tag"])
            while True:
                if build_image(image_dict["path"], image_dict["dockerfile"], image_dict["image_tag"]):
                    print("build successfully on {0}".format(image_dict["image_tag"]))
                    break
                else:
                    print("on_sleep")
                    sleep(45)
        else:
            print("image exist installation skipped")
            return True
    return True


def httprobe_exec(local_client, image_tag):
    resp = local_client.containers.run(image_tag,
                                       volumes={
                                           '/tmp/httprobe_scan': {
                                               'bind': '/dev/shm', 'mode': 'rw'}})

    print(resp)
    return resp


if __name__ == '__main__':
    def main():
        image_tag_list = [{'path': '.',
                           "dockerfile": "Dockerfile.httprobe",
                           'image_tag': 'httprobe'}
                          ]


        force_installation_dockers(image_tag_list)
        print("sleeped")
        sleep(3)

        httprobe_exec(client, "httprobe")

    main()
