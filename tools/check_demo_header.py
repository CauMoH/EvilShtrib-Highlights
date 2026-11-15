with open(r'c:\Users\CauMo\source\repos\EvilShtrib-Highlights\demos\auto-2611141954-zm_lb.dem', 'rb') as f:
    magic = f.read(8)
    demo_protocol = int.from_bytes(f.read(4), 'little')
    net_protocol = int.from_bytes(f.read(4), 'little')
    map_name = f.read(260).split(b'\x00')[0].decode('latin1')
    game_dir = f.read(260).split(b'\x00')[0].decode('latin1')
    map_crc = int.from_bytes(f.read(4), 'little')
    print(f'Magic: {magic}, DemoProt: {demo_protocol}, NetProt: {net_protocol}, Map: "{map_name}", Game: "{game_dir}"')
