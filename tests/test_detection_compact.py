"""Contract test using the repository's own XML and official generator."""
import importlib.util
from pathlib import Path
import sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from generator import mavgen

class CompactContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();path=Path(cls.temp.name)/'dialect.py'
        assert mavgen.mavgen(mavgen.Opts(str(path),wire_protocol='2.0',language='Python3'),[str(ROOT/'message_definitions/v1.0/common.xml')])
        spec=importlib.util.spec_from_file_location('compact_test_dialect',path)
        cls.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.module)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def test_layout_crc_and_endpoints(self):
        m=self.module;tx=m.MAVLink(None,srcSystem=191,srcComponent=190)
        wire=tx.plane_detection_compact_encode(255,255,255,255).pack(tx)
        self.assertEqual(wire[10:14],bytes([255]*4));self.assertEqual(wire[1],4)
        cls=m.mavlink_map[61000];self.assertEqual(cls.crc_extra,152)
        rx=m.MAVLink(None).parse_char(wire);self.assertEqual(rx.to_dict()['center_y'],255)
    def test_zero_trim_and_cancel(self):
        m=self.module;tx=m.MAVLink(None)
        for fields,length in [((0,7,0,0),2),((0,0,0,0),1),((1,1,0,0),2)]:
            wire=tx.plane_detection_compact_encode(*fields).pack(tx)
            self.assertEqual(wire[1],length)
            rx=m.MAVLink(None).parse_char(wire)
            self.assertEqual((rx.record_index,rx.track_id,rx.center_x,rx.center_y),fields)
    def test_legacy_messages_preserved(self):
        m=self.module
        self.assertEqual(m.mavlink_map[3].msgname,'PLANE_TARGET_BBOX')
        self.assertEqual(m.mavlink_map[9].crc_extra,237)
        self.assertEqual(m.mavlink_map[10].crc_extra,41)

if __name__=='__main__':unittest.main()
