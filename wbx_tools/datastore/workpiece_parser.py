import re
import shlex


class WorkPiece:
    def __init__(self, workpiece: str):
        self._columns = workpiece.split("|")
        if len(self._columns) == 6:
            self._search_query = self._columns[0]
            self._norm_query = self._columns[1]
            self._miner = self._columns[2]
            self._miner_args = self._columns[3]
            self._query = self._columns[4]
            self._shard_kind = self._columns[5]
        else:
            self._search_query = ""
            self._norm_query = ""
            self._miner = ""
            self._miner_args = ""
            self._query = ""
            self._shard_kind = ""

    def parse_miner_args(self):
        if len(self._columns) == 1:
            return {"query": "|".join(self._columns)}

        try:
            args_field = shlex.split(self._miner_args)

        except ValueError as err:
            # logger.warning(f"ValueError: {err}")
            return None
        except Exception as err:
            # logger.error(err)
            return None

        json_body = dict()

        if self._miner == "catalog":
            urls = list()
            if "@sort" in self._miner_args:
                args_field, sort_args = self._miner_args.split(" @sort: ")
                args_field = shlex.split(args_field)

                sort_args = shlex.split(sort_args)
                json_body["sortParameters"] = dict()
                for sort_arg in sort_args:
                    key, value = sort_arg.split("=")

                    if value.isdigit():
                        value = int(value)

                    if value == "true" or value == "True":
                        value = True
                    elif value == "false" or value == "False":
                        value = False
                    elif value == "-1":
                        value = -1

                    json_body["sortParameters"][cmd_arg_name_merger(key, True)] = value

            for arg in args_field:
                if arg.startswith("http"):
                    urls.append(arg)
                elif len(arg.split("=")) == 1 and not arg.startswith("http"):
                    json_body[cmd_arg_name_merger(arg)] = True
                else:
                    key, value = arg.split("=")
                    if value.isdigit():
                        value = int(value)

                    if value == "true" or value == "True":
                        value = True
                    elif value == "false" or value == "False":
                        value = False
                    elif value == "-1":
                        value = -1

                    json_body[cmd_arg_name_merger(key)] = value

            json_body["URLs"] = urls

            return json_body

        if "@sort" in self._miner_args:
            args_field, sort_args = self._miner_args.split(" @sort: ")
            args_field = shlex.split(args_field)

            sort_args = shlex.split(sort_args)
            json_body["sortParameters"] = dict()
            for sort_arg in sort_args:
                key, value = sort_arg.split("=")

                if value.isdigit():
                    value = int(value)

                if value == "true" or value == "True":
                    value = True
                elif value == "false" or value == "False":
                    value = False
                elif value == "-1":
                    value = -1

                json_body["sortParameters"][cmd_arg_name_merger(key, True)] = value

        for arg in args_field:
            key, value = arg.split("=")

            if value.isdigit():
                value = int(value)

            if value == "true" or value == "True":
                value = True
            elif value == "false" or value == "False":
                value = False
            elif value == "-1":
                value = -1

            json_body[cmd_arg_name_merger(key)] = value

        return json_body

    @property
    def get_search_query(self):
        return self._search_query

    @property
    def get_norm_query(self):
        return self._norm_query

    # @property
    # def get_preset_id(self):
    #     print(self._columns)
    #     if len(self._columns) == 1:
    #         self._search_query = "|".join(self._columns)
    #
    #     print(self._search_query)
    #
    #     master_part_info = master_part(self._search_query, query_type="by_human_query")
    #
    #     if master_part_info:
    #         shard_query = master_part_info.get("ShardQuery")
    #
    #         preset_id = re.compile(r"preset=(\d+)")
    #         match = re.search(preset_id, shard_query)
    #
    #         if match:
    #             return int(match.groups()[0])
    #         return 0
    #     return 123456987

    @property
    def get_miner(self):
        return self._miner

    @property
    def get_query(self):
        return self._query

    @property
    def get_shard_kind(self):
        return self._shard_kind


def cmd_arg_name_merger(arg: str, sort: bool = False):
    name = ""

    if "context-subject-filter" in arg:
        return "contextFilter"

    if "--context-brand-filter" in arg:
        return "brandFilter"

    word_list = arg.replace("--", "").split("-")
    for word in word_list:
        if word_list.index(word) == 0:
            if sort:
                name += word.capitalize()
                continue
            name += word
        else:
            name += word.capitalize()

    return name
