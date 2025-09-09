# Simulasi Sistem Lift
#
# Program ini mensimulasikan operasi beberapa lift di sebuah gedung.
# Pengguna memberikan input untuk jumlah lift, jumlah lantai,
# dan kapasitas muatan tiap lift, dan sistem mensimulasikan bagaimana lift
# bergerak berdasarkan permintaan penumpang.
#
# Kamus:
#   - Titlecard (str): Judul besar program
#   - lifts (list): Daftar yang berisi objek lift. Setiap objek lift berisi:
#       - floor (int): Posisi lantai lift saat ini.
#       - load (int): Jumlah orang yang ada di dalam lift saat ini.
#       - target (int): Lantai target yang ingin dituju lift.
#       - is_used (bool): Flag yang menandakan apakah lift sedang digunakan.
#       - queue (list): Daftar lantai yang harus dikunjungi lift untuk perjalanan tambahan.
#   - lift_amount (int): Jumlah lift yang ada di gedung.
#   - lift_loadlimit (int): Batas maksimum muatan (jumlah orang) yang bisa ditampung oleh lift.
#   - floor_amount (int): Jumlah lantai yang ada di gedung./
#   - mode (int): memilih mode (1 = input real, 2 = simulasi)
#   - time_spent (list): Daftar yang berisi perhitungan waktu untuk setiap lift, dengan:
#       - time_spent[x][0] (int): Waktu yang dibutuhkan lift untuk memenuhi permintaan.
#       - time_spent[x][1] (int): Jenis pergerakan (0: arah yang sama, 1: arah yang sama dalam jarak tertentu, 2: arah berbeda).
#   - temp_floor (int): Variabel sementara untuk menyimpan lantai lift saat inisialisasi.
#   - temp_load (int): Variabel sementara untuk menyimpan jumlah muatan lift saat inisialisasi.
#   - temp_target (int): Variabel sementara untuk menyimpan lantai target lift saat inisialisasi.
#   - cur_floor (int): Lantai saat ini dari pengguna yang meminta lift.
#   - cur_people (int): Jumlah orang yang terdeteksi oleh sistem di lantai saat ini.
#   - cur_target (int): Lantai target dari pengguna yang meminta lift.
#   - available (bool): Flag yang menandakan apakah ada lift yang tersedia.
#   - fastest (int): Indeks lift tercepat yang akan memenuhi permintaan saat ini.
#
# Fungsi:
#   - lift.returnmove(): Menentukan pergerakan lift: diam (s), naik (u), atau turun (d).
#   - lift.move(): Memindahkan lift menuju lantai target.
#   - visualize_lifts(lifts, floor_amount): Memvisualisasikan posisi dan status setiap lift.
#   - AskInput(check, prompt, limits): Meminta input dan memastikan input tidak menimbulkan error di program
#   - main loop: Menangani input pengguna dan mengendalikan permintaan serta pergerakan lift.
import sys, random, time

titlecard = """
=============================================================================
     .-') _    ('-.             .-. .-')             _ (`-. .-. .-')
    ( OO ) )  ( OO ).-.         \  ( OO )           ( (OO  )\  ( OO )
,--./ ,--,'   / . --. /  ,-.-') ,--. ,--.  ,-.-')  _.`     \,--. ,--.
|   \ |  |\   | \-.  \   |  |OO)|  .'   /  |  |OO)(__...--''|  .'   /
|    \|  | ).-'-'  |  |  |  |  \|      /,  |  |  \ |  /  | ||      /,
|  .     |/  \| |_.'  |  |  |(_/|     ' _) |  |(_/ |  |_.' ||     ' _)
|  |\    |    |  .-.  | ,|  |_.'|  .   \  ,|  |_.' |  .___.'|  .   \\
|  | \   |    |  | |  |(_|  |   |  |\   \(_|  |    |  |     |  |\   \\
`--'  `--'    `--' `--'  `--'   `--' '--'  `--'    `--'     `--' '--'

                    v 1.4
                    Jangan liftnya doang yang naik bre...
=============================================================================
"""
print(titlecard)

class lift:
    def __init__(self, floor, load, target):
        # Inisialisasi objek lift
        self.floor = floor  # Lokasi lift sekarang
        self.load = load  # Beban di lift sekarang
        self.target = target  # Tujuan lift sekarang
        self.is_used = False  # Indikator apakah lift sedang digunakan untuk beberapa trip
        self.queue = []  # Barisan beberapa trip lift
        self.operational_hours = 0
        self.trips_count = 0
        self.max_operational_hours = 1000
        self.max_trips_count = 10000
        self.service_history = []

    def returnmove(self):
        # Menentukan pergerakan lift, s = stationary, u = up, d = down
        if self.target == self.floor:
            self.load = 0
            return 's'
        return 'd' if self.target - self.floor < 0 else 'u'

    def move(self):
        # Mengerakkan lift menuju targetnya
        if self.returnmove() == 'd':
            self.floor -= 1  # Ke atas
        elif self.returnmove() == 'u':
            self.floor += 1  # Ke bawah
        else:
            # Ketika berhenti, mengecek jika misalkan ada target lainnya di barisan queue
            if self.is_used:
                if not self.queue:  # Kalau kosong, bearti lift sudah siap digunakan untuk beberapa trip
                    self.is_used = False
                else:
                    # Mengubah target berdasarkan queue
                    self.target = self.queue.pop(0)
                    # Mulai menggerakkan lift kembali
                    if self.returnmove() == 'd':
                        self.floor -= 1
                    elif self.returnmove() == 'u':
                        self.floor += 1
    def use_lift(self, hours, trips):
        self.operational_hours += hours
        self.trips_count =+ trips
        print(f"Lift already been used for {hours} hours and {trips} trips")

    def check_service_due(self):
        if self.operational_hours >= self.max_operational_hours:
          print(f"Warning! lift neef to be serviced")
          self.schedule_service()
        elif self.trips_count >= self.max_trips_count:
          print(f"Warning! lift need to be serviced")
        else:
          print(f"Life still in a good condition")

    def schedule_service(self):
        service_date = time.strftime("%y-%m-%d %H:%M:%S", time.localtime())
        self.service_history.append(service_date)
        print(f"Service scheduled to be  {service_date}.\n")
        self.operational_hours = 0
        self.travel_count = 0

    def show_service_history(self):
        if self.service_history:
            print("Service History:")
            for service in self.service_history:
                print(service)

def visualize_lifts(lifts, floor_amount, desc_on):        ### BARU 0 (ADA DIKIT YANG KUGANTI, KUTAMBAHIN DESC ON)
    # Visualisasi posisi lift di setiap lantai
    lift_positions = [[" " for _ in range(len(lifts))] for _ in range(floor_amount)]
    for i, lift in enumerate(lifts):
        lift_positions[floor_amount - lift.floor][i] = "L"  # Penandaan posisi lift
    print("\nLift Visualization:")
    for i in range(floor_amount):
        # Penampilan lantai
        floor_number = f"Floor {floor_amount - i}".ljust(8)
        floor_representation = "|" + "|".join(lift_positions[i]) + "|"
        print(f"{floor_number} {floor_representation}")
    # Penampilan status setiap lift                       ### PENAMPILAN STATUS SETIAP LIFT ADA KUMODIF JUGA
    lift_representation = "Lifts :   1"
    if len(lifts) > 9:
        for i in range(2,len(lifts)+1):
            lift_representation = lift_representation + " " + str(i)
    else:
        lift_representation = "Lifts :   1 2 3 4 5 6 7 8 9 ..."
    print(lift_representation)
    if desc_on.lower() == 'y':
        for i in range(lift_amount):
            status = "(NOT AVAILABLE)" if lifts[i].is_used else "AVAILABLE"
            print(f"Lift-{i + 1}. Floor: {lifts[i].floor} | Target: {lifts[i].target} | Load: {lifts[i].load} | Status: {status}")

### BARU 1
def AskInput(check, prompt, limits):
    # Meminta input untuk setiap variabel dan memastikan input tidak menimbulkan error
    git = ""
    if isinstance(check, int):
        git = limits[0] - 1
        counter = 0
        while git not in range(limits[0], limits[1]+1):
            if counter > 0:
                print("Input isn't in the given limits (" + str(limits[0]) + " - " + str(limits[1]) + ")")
            try:
                git = int(input(prompt))
            except ValueError:
                print("Make sure your input is an integer")
            counter += 1
    if isinstance(check, str):
        counter = 0
        while git not in limits:
            if counter > 0:
                print("Input isn't in the given limits " + str(limits))
            git = input(prompt)
            counter += 1
    return git


###

# Variabel input pengguna terkait kondisi awal
temp_floor = 0
temp_load = 0
temp_target = 0
cur_floor = 0
cur_people = 0
cur_target = 0
lifts = []
lift_amount = AskInput(0, "How many lifts are there? ", (1, sys.maxsize))  # Jumlah lift
lift_loadlimit = AskInput(0, "How many people can one lift hold? ", (1, sys.maxsize))# Batasan spesifikasi lift
floor_amount = AskInput(0, "How many floors are there? ", (1, sys.maxsize)) # Jumlah lantai
time_spent = [[0, 0] for i in range(lift_amount)]  # Pengecek waktu yang dibutuhkan setiap lift

#time_spent[[x,y]], x menandakan waktu yang dibutuhkan untuk memenuhi permintaan, sementara y menandakan jenis gerak yang dilalui (lebih rinci dibawah)

### BARU 2
print("=============================================================================")
print("\t\tSELECT MODES::")
print("\t\t1. INPUT REAL")
print("\t\t2. SIMULATION")
print("\t\t3. SERVICE")
mode = AskInput(0, "Input: ", (1,3))
print("=============================================================================")
# Inisialisasi objek lift
if mode == 1:
    for i in range(lift_amount):
        print(f"For lift {i + 1}:")
        temp_floor = AskInput(0, "Floor: ", (1, floor_amount))
        temp_target = AskInput(0, "Heading to Floor: ", (1, floor_amount))
        temp_load = AskInput(0, "Load: ", (1, lift_loadlimit))
        lifts.append(lift(temp_floor, temp_load, temp_target))
elif mode == 2:
    for i in range(lift_amount):
        temp_floor = random.randint(1, floor_amount)
        temp_target = random.randint(1, floor_amount)
        temp_load = random.randint(1,lift_loadlimit)
        lifts.append(lift(temp_floor, temp_load, temp_target))

###

# Main loop
if mode == 1:
    while True:
        visualize_lifts(lifts, floor_amount, 'y')
        print("-- Insert Data --")
        cur_floor = input("(input xxx to stop |Enter to continue) Current floor: ")
        if cur_floor == 'xxx':  # kondisi terminasi
            break
        elif cur_floor == '':
            # Menggerakkan semua lift (ibarat 1 satuan waktu berlewat dan tidak ada yang memencet)
            for i in range(lift_amount):
                lifts[i].move()
        else:
            # Menerima input
            cur_floor = int(cur_floor)
            if cur_floor < 1 or cur_floor > floor_amount:
                print("Input isn't in the given limits (1 - " + str(floor_amount) + ")")
                cur_floor = AskInput(0, "Input Current Floor: ", (1, floor_amount))
            cur_people = AskInput(0,"Amount of people detected: ", (1,sys.maxsize))
            cur_direction = AskInput('0', "Up or Down? (u/d)", ('u','d','U','D'))
            cur_target = AskInput(0, "Heading to floor: ", (1,floor_amount))
            for i in range(lift_amount):
                # Kalkulasi waktu yang dibutuhkan setiap lift untuk memenuhi request
                if cur_direction == lifts[i].returnmove():
                    # Ketika lift bergerak searah
                    if (lifts[i].returnmove() == 'u' and cur_floor < lifts[i].floor) or (lifts[i].returnmove() == 'd' and cur_floor > lifts[i].floor):
                        # Ketika penumpang berada di luar jangkauan gerak lift (Jarak lift ke penumpang)
                        time_spent[i][0] = abs(lifts[i].target - lifts[i].floor) + abs(lifts[i].target - cur_floor)
                        time_spent[i][1] = 0
                    else:
                        # Ketika penumpang berada di dalam jangkauan gerak lift (Jarak lift ke penumpang)
                        time_spent[i][0] = abs(cur_floor - lifts[i].floor)
                        time_spent[i][1] = 1
                else:
                    # Ketika lift bergerak beda arah (Lift ke target dulu, baru dari target ke penumpang)
                    time_spent[i][0] = abs(lifts[i].target - lifts[i].floor) + abs(lifts[i].target - cur_floor)
                    time_spent[i][1] = 2
                # time_spent[x][1] menandakan jenis gerak, 0 = searah, di luar jangkauan, 1 = searah, di dalam jangkauan, 2 = berbeda arah

                # Mengecek kondisi overload
                if lifts[i].load + cur_people > lift_loadlimit:
                    # Menambah waktu sesuai dengan berapa trip yang dibutuhkan
                    time_spent[i][0] += ((lifts[i].load + cur_people) // lift_loadlimit) * 2 * max(abs(cur_floor - cur_target), abs(cur_floor - lifts[i].target))
            print(time_spent)
            available = True
            # Mengecek ketersediaan lift
            for i in range(len(time_spent)):
                if not lifts[i].is_used:
                    fastest = i
                    break
                if i == len(time_spent) - 1:
                    print("NO LIFTS ARE AVAILABLE AT THE MOMENT, PLEASE WAIT")
                    available = False
            # Menentukan lift yang tercepat
            if available:
                for i in range(len(time_spent)):
                    if time_spent[i][0] < time_spent[fastest][0] and not lifts[i].is_used:
                        fastest = i

                # Mengubah target sesuai dengan jenis gerak
                if time_spent[fastest][1] == 0:
                    lifts[fastest].queue.append(cur_floor)
                    lifts[fastest].queue.append(cur_target)
                    lifts.is_used = True
                elif time_spent[fastest][1] == 1:
                    if abs(lifts[fastest].target-cur_floor) < abs(cur_target-cur_floor):
                        lifts[fastest].target = cur_target
                elif time_spent[fastest][1] == 2:
                    lifts[fastest].queue.append(cur_floor)
                    lifts[fastest].queue.append(cur_target)
                    lifts[fastest].is_used = True
                # Menambahkan ke queue untuk kasus overload
                if lifts[fastest].load + cur_people > lift_loadlimit:
                    trips = (lifts[fastest].load + cur_people) // lift_loadlimit
                    for i in range(trips):
                        lifts[fastest].queue.append(cur_floor)
                        lifts[fastest].queue.append(lifts[fastest].target)
                        lifts[fastest].is_used=True
                lifts[fastest].load = min(20, lifts[fastest].load + cur_people)
            # Menggerakkan semua lift
            for i in range(lift_amount):
                lifts[i].move()
## BARU 3
elif mode == 2:
    desc_on = AskInput("0", "Do you want descriptions on? (y/n)", ('y', 'Y', 'n', 'N'))
    while True:
        visualize_lifts(lifts, floor_amount, desc_on)
        cur_floor = random.randint(0,1) # 1/2 kemungkinan untuk tidak ada penumpang
        if cur_floor == '0':
            # Menggerakkan semua lift (ibarat 1 satuan waktu berlewat dan tidak ada yang memencet)
            print("NO INPUT")
            for i in range(lift_amount):
                lifts[i].move()
        else:
            cur_floor = random.randint(1,floor_amount)
            cur_people = random.randint(1,lift_loadlimit)
            cur_target = random.randint(1,floor_amount)
            if cur_target > cur_people:
                cur_direction = 'u'
            else:
                cur_direction = 'd'
            print(f"SIMULATED INPUT: {cur_people} from FLOOR {cur_floor} heading to FLOOR {cur_target}")
            for i in range(lift_amount):
                # Kalkulasi waktu yang dibutuhkan setiap lift untuk memenuhi request
                if cur_direction == lifts[i].returnmove():
                    # Ketika lift bergerak searah
                    if (lifts[i].returnmove() == 'u' and cur_floor < lifts[i].floor) or (lifts[i].returnmove() == 'd' and cur_floor > lifts[i].floor):
                        # Ketika penumpang berada di luar jangkauan gerak lift (Jarak lift ke penumpang)
                        time_spent[i][0] = abs(lifts[i].target - lifts[i].floor) + abs(lifts[i].target - cur_floor)
                        time_spent[i][1] = 0
                    else:
                        # Ketika penumpang berada di dalam jangkauan gerak lift (Jarak lift ke penumpang)
                        time_spent[i][0] = abs(cur_floor - lifts[i].floor)
                        time_spent[i][1] = 1
                else:
                    # Ketika lift bergerak beda arah (Lift ke target dulu, baru dari target ke penumpang)
                    time_spent[i][0] = abs(lifts[i].target - lifts[i].floor) + abs(lifts[i].target - cur_floor)
                    time_spent[i][1] = 2
                # time_spent[x][1] menandakan jenis gerak, 0 = searah, di luar jangkauan, 1 = searah, di dalam jangkauan, 2 = berbeda arah

                # Mengecek kondisi overload
                if lifts[i].load + cur_people > lift_loadlimit:
                    # Menambah waktu sesuai dengan berapa trip yang dibutuhkan
                    time_spent[i][0] += ((lifts[i].load + cur_people) // lift_loadlimit) * 2 * max(
                        abs(cur_floor - cur_target), abs(cur_floor - lifts[i].target))
            available = True
            # Mengecek ketersediaan lift
            for i in range(len(time_spent)):
                if not lifts[i].is_used:
                    fastest = i
                    break
                if i == len(time_spent) - 1:
                    print("NO LIFTS ARE AVAILABLE AT THE MOMENT, PLEASE WAIT")
                    available = False
            # Menentukan lift yang tercepat
            if available:
                for i in range(len(time_spent)):
                    if time_spent[i][0] < time_spent[fastest][0] and not lifts[i].is_used:
                        fastest = i

                # Mengubah target sesuai dengan jenis gerak
                if time_spent[fastest][1] == 0:
                    lifts[fastest].queue.append(cur_floor)
                    lifts[fastest].queue.append(cur_target)
                    lifts.is_used = True
                elif time_spent[fastest][1] == 1:
                    if abs(lifts[fastest].target - cur_floor) < abs(cur_target - cur_floor):
                        lifts[fastest].target = cur_target
                elif time_spent[fastest][1] == 2:
                    lifts[fastest].queue.append(cur_floor)
                    lifts[fastest].queue.append(cur_target)
                    lifts[fastest].is_used = True
                # Menambahkan ke queue untuk kasus overload
                if lifts[fastest].load + cur_people > lift_loadlimit:
                    trips = (lifts[fastest].load + cur_people) // lift_loadlimit
                    for i in range(trips):
                        lifts[fastest].queue.append(cur_floor)
                        lifts[fastest].queue.append(lifts[fastest].target)
                        lifts[fastest].is_used = True
                lifts[fastest].load = min(20, lifts[fastest].load + cur_people)
            # Menggerakkan semua lift
            for i in range(lift_amount):
                lifts[i].move()
            time.sleep(2)

elif mode == 3:
        print("\t\tSELECT MODES::")
        print("\t\t1. Lift Usage")
        print("\t\t2. Check lift service status")
        print("\t\t3. Service History")
        mode = AskInput(0, "Input: ", (1,3))

        if mode == 1 :
           lift_index = int(input(f"Input lift number (1-{lift_amount}): ")) - 1
           if 0 <= lift_index < lift_amount:
              hours = int(input("Input lift usage amount of hours: "))
              trips = int(input("lift amount of trips: "))
              lifts[lift_index].use_lift(hours, trips)
              lifts[lift_index].check_service_due()
           else:
              print("invalid lift number")


##
