"""
    Copyright (c) 2016 Ad Schellevis
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
    AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

    --------------------------------------------------------------------------------------
    data aggregator type
"""
from lib.aggregate import BaseFlowAggregator

class FlowInterfaceTotals(BaseFlowAggregator):
    """ collect interface totals
    """
    target_filename = '/var/netflow/interface_%06d.sqlite'
    agg_fields = ['if', 'direction']

    @classmethod
    def resolutions(cls):
        """
        :return: list of sample resolutions
        """
        # sample in 30 seconds, 5 minutes, 1 hour and 1 day
        return  [30, 300, 3600, 86400]

    @classmethod
    def history_per_resolution(cls):
        """
        :return: dict sample resolution / expire time (seconds)
        """
        return  {30: cls.seconds_per_day(1),
                 300: cls.seconds_per_day(7),
                 3600: cls.seconds_per_day(31),
                 86400: cls.seconds_per_day(365)
                 }

    def __init__(self, resolution):
        """
        :param resolution: sample resultion (seconds)
        :return: None
        """
        super(FlowInterfaceTotals, self).__init__(resolution)

    def add(self, flow):
        """ combine up/down flow into interface and direction
        :param flow: netflow data
        :return: None
        """
        flow['if'] = flow['if_in']
        flow['direction'] = 'out'
        flow_copy = self.copy_reverse_flow(flow)
        flow_copy['if'] = flow_copy['if_in']
        flow_copy['direction'] = 'in'
        super(FlowInterfaceTotals, self).add(flow)
        super(FlowInterfaceTotals, self).add(flow_copy)