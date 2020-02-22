'''
@Author: WangGuanran
@Email: wangguanran@vanzotec.com
@Date: 2020-02-21 11:03:15
@LastEditTime: 2020-02-22 16:02:15
@LastEditors: WangGuanran
@Description: Project manager py file
@FilePath: \vprojects\vprjcore\project_manager.py
'''
import os
import sys
import json

from vprjcore.common import log, list_file_path

PROJECT_INFO_PATH = "./.cache/project_info.json"


class ProjectManager(object):

    '''
    Singleton mode
    '''
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()

    def before_new_project(self, project):
        project.by_new_project_base = False
        base_name = project.args_dict.pop("base", None)
        if base_name is None:
            log.error("You need to use '--base' to specify platform information")
            sys.exit(-1)
        else:
            project.base_name = base_name
        log.debug("base name = %s" % (base_name))

        for dirname in list_file_path("new_project_base", max_depth=1, only_dir=True):
            if os.path.basename(dirname).upper() == base_name.upper():
                project.platform_name = base_name.upper()
                project.by_new_project_base = True
                return True

        json_info = json.load(open(PROJECT_INFO_PATH, "r"))
        for prj_name, temp_info in json_info.items():
            if prj_name == base_name:
                project.platform_name = temp_info["platform_name"]
                return True

    def after_new_project(self, project):
        # save project info
        prj_info = {}
        json_info = {}
        except_list = [
            "args_dict",
            "platform_handler",
            "plugin_list",
            "operate",
        ]
        try:
            json_info = json.load(open(PROJECT_INFO_PATH, "r"))
        except:
            log.debug("%s is null"%(PROJECT_INFO_PATH))
        for attr in dir(project):
            var = getattr(project, attr)
            if not (callable(var) or attr.startswith("_") or attr in except_list):
                prj_info[attr] = var
        json_info[project.project_name] = prj_info
        json.dump(json_info, open(PROJECT_INFO_PATH, "w+"), indent=4)

    def before_compile_project(self, project_name, is_debug=False):
        '''
        @description: get project information from cache file or db
        @param {type} project_name:project name(str)
        @return: project info(dict)
        '''
        prj_info = None

        if is_debug:
            self._create_fake_info(project_name)
        # TODO Query the database to confirm whether the project data is updated
        # If yes, update the cache file. If no project information is found, an error will be returned
        log.debug("query database")
        # Save project info into cache(PROJECT_INFO_PATH)
        # with open(PROJECT_INFO_PATH, "w+") as f_write:
        #     json.dump(prj_info, f_write)
        #     f_write.write("\n")
        # END

        # Search project info in PROJECT_INFO_PATH first
        if os.path.exists(PROJECT_INFO_PATH):
            json_info = json.load(open(PROJECT_INFO_PATH, "r"))
            for prj_name, temp_info in json_info.items():
                if(prj_name.lower() == project_name.lower()):
                    prj_info = temp_info

        if prj_info is None:
            log.warning("The project('%s') info is None" % (project_name))
        else:
            prj_info["name"] = project_name.lower()
            log.info("prj_info = %s" % (prj_info))
        return prj_info

    def _create_fake_info(self, project_name):
        '''
        @description: Create some fake information to debug(write to json file)
        @param {type} args_dict:parameter list
        @return: None
        '''
        json_info = {}
        prj_info = {}
        if os.path.exists(PROJECT_INFO_PATH):
            with open(PROJECT_INFO_PATH, "r") as f_read:
                try:
                    if os.path.getsize(PROJECT_INFO_PATH):
                        json_info = json.load(f_read)
                    else:
                        log.warning("json file size is zero")
                except:
                    log.exception("Json file format error")
                f_read.close()

        for prj_name, temp_info in json_info.items():
            if(prj_name == project_name):
                prj_info = temp_info
        if len(prj_info) == 0:
            log.debug("Insert fake project info")
            # prj_info["name"] = project_name
            prj_info["kernel_version"] = 3.18
            prj_info["android_version"] = 7.0
            prj_info["platform_name"] = "MT6735"

            json_info[project_name.lower()] = prj_info
            with open(PROJECT_INFO_PATH, "w+") as f_write:
                json.dump(json_info, f_write, indent=4)
                f_write.close()
        else:
            log.debug("project info is already exist,skip this step")


def get_module():
    return ProjectManager()
