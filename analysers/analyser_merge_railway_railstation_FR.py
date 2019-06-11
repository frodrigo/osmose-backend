#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2012                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from .Analyser_Merge import Analyser_Merge, Source, GTFS, Load, Mapping, Select, Generate


class Analyser_Merge_Railway_Railstation_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"1072", "class": 1, "level": 1, "tag": ["missing_official", "fix:imagery", "railway"], "desc": T_(u"Railway station not integrated") }
        self.missing_osm      = {"item":"1073", "class": 2, "level": 1, "tag": ["missing_osm", "fix:imagery", "railway"], "desc": T_(u"Railway station without tag \"uic_ref\" or invalid") }
        self.possible_merge   = {"item":"1074", "class": 3, "level": 1, "tag": ["possible_merge", "fix:imagery", "railway"], "desc": T_(u"Railway station, integration suggestion") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://ressources.data.sncf.com/explore/dataset/sncf-ter-gtfs/",
            u"Horaires prévus des trains TER",
            GTFS(Source(attribution = u"SNCF", millesime = "08/2017",
                    fileUrl = u"https://ressources.data.sncf.com/explore/dataset/sncf-ter-gtfs/files/24e02fa969496e2caa5863a365c66ec2/download/")),
            Load("stop_lon", "stop_lat",
                select = {"stop_id": "StopPoint:OCETrain%"}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"railway": ["station", "halt"]}),
                osmRef = "uic_ref",
                conflationDistance = 500,
                generate = Generate(
                    static1 = {
                        "railway": "station",
                        "operator": "SNCF"},
                    static2 = {"source": self.source},
                    mapping1 = {"uic_ref": lambda res: res["stop_id"].split(":")[1][3:].split("-")[-1][:-1]},
                    mapping2 = {"name": lambda res: res["stop_name"].replace("gare de ", "")},
                    text = lambda tags, fields: {"en": fields["stop_name"][0].upper() + fields["stop_name"][1:]} )))
