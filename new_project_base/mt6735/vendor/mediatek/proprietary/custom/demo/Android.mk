LOCAL_PATH:= $(call my-dir)
ifeq ($(MTK_PROJECT), demo)
include $(call all-makefiles-under,$(LOCAL_PATH))
endif
