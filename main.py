import os
import sys
import time
from examples import simple_demo, fragmentation_demo, metrics_demo
from src.simulation.simulator import Simulator
from src.visualization.disk_render import DiskRenderer
from src.metrics.fragmentation_metrics import FragmentationMetrics

# Códigos de cores ANSI para um visual premium no terminal
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(f"{BLUE}{BOLD}============================================================{RESET}")
    print(f"{BLUE}{BOLD}         SIMULADOR DE ALOCAÇÃO CONTÍGUA DE BLOCOS            {RESET}")
    print(f"{BLUE}{BOLD}============================================================{RESET}")


def run_interactive():
    clear_screen()
    print_banner()
    print(f"\n{CYAN}--- INICIANDO SIMULAÇÃO INTERATIVA ---{RESET}\n")

    # Obter tamanho do disco com validação de entrada
    while True:
        try:
            size_input = input("Digite o tamanho do disco em blocos (padrão 16): ").strip()
            if size_input == "":
                disk_size = 16
                break
            disk_size = int(size_input)
            if disk_size <= 0:
                print(f"{RED}O tamanho do disco deve ser maior que zero.{RESET}")
                continue
            break
        except ValueError:
            print(f"{RED}Entrada inválida. Digite um número inteiro.{RESET}")

    sim = Simulator(disk_size)
    renderer = DiskRenderer()

    while True:
        clear_screen()
        print_banner()
        print(f"\n{CYAN}--- MODO INTERATIVO (Disco de {disk_size} blocos) ---{RESET}\n")

        # Renderiza o disco graficamente no terminal
        renderer.render(sim.disk)

        # Exibe métricas de desempenho em tempo real
        metrics = FragmentationMetrics(sim.disk).generate_report()
        print(f"{BOLD}📊 Métricas em Tempo Real:{RESET}")
        print(f"  • Taxa de Ocupação: {YELLOW}{metrics['occupancy_rate']:.1f}%{RESET}")
        print(f"  • Espaço Livre Total: {GREEN}{metrics['free_blocks']} bloco(s){RESET}")
        print(f"  • Maior Região Livre Contígua: {GREEN}{metrics['largest_free_region']} bloco(s){RESET}")
        print(
            f"  • Fragmentação Externa: {RED if metrics['external_fragmentation'] > 0 else GREEN}{metrics['external_fragmentation']:.1f}%{RESET}"
        )
        print("-" * 60)

        # Menu de opções da simulação
        print(f"{BOLD}Opções:{RESET}")
        print(f"  [{GREEN}1{RESET}] Criar/Alocar Arquivo")
        print(f"  [{GREEN}2{RESET}] Deletar/Desalocar Arquivo")
        print(f"  [{GREEN}3{RESET}] Listar Arquivos Alocados")
        print(f"  [{GREEN}4{RESET}] Voltar ao Menu Principal")

        choice = input(f"\n{BOLD}Escolha uma opção (1-4): {RESET}").strip()

        if choice == "1":
            name = input("Nome do arquivo (ex: arqA): ").strip()
            if not name:
                print(f"{RED}Nome do arquivo não pode ser vazio!{RESET}")
                input("\nPressione Enter para continuar...")
                continue
            try:
                size = int(input("Tamanho do arquivo em blocos: ").strip())
                if size <= 0:
                    print(f"{RED}O tamanho deve ser maior que zero!{RESET}")
                    input("\nPressione Enter para continuar...")
                    continue
            except ValueError:
                print(f"{RED}Tamanho inválido! Digite um número inteiro.{RESET}")
                input("\nPressione Enter para continuar...")
                continue

            try:
                success = sim.create_file(name, size)
                if success:
                    print(f"\n{GREEN}✔ Arquivo '{name}' alocado com sucesso!{RESET}")
                else:
                    print(
                        f"\n{RED}❌ FALHA NA ALOCAÇÃO: Não há região contígua livre de tamanho {size}!{RESET}"
                    )
                    if metrics["free_blocks"] >= size:
                        print(
                            f"{YELLOW}👉 Nota: O disco possui {metrics['free_blocks']} blocos livres totais, mas eles não estão contíguos (Fragmentação Externa).{RESET}"
                        )
            except Exception as e:
                print(f"\n{RED}Erro: {e}{RESET}")
            input("\nPressione Enter para continuar...")

        elif choice == "2":
            name = input("Nome do arquivo a ser deletado: ").strip()
            if not name:
                print(f"{RED}Nome do arquivo não pode ser vazio!{RESET}")
                input("\nPressione Enter para continuar...")
                continue
            success = sim.delete_file(name)
            if success:
                print(f"\n{GREEN}✔ Arquivo '{name}' removido e espaço liberado!{RESET}")
            else:
                print(f"\n{RED}❌ Erro: Arquivo '{name}' não encontrado.{RESET}")
            input("\nPressione Enter para continuar...")

        elif choice == "3":
            files = sim.list_files()
            print(f"\n{BOLD}📂 Arquivos Alocados:{RESET}")
            if not files:
                print("  Nenhum arquivo alocado no momento.")
            else:
                for f in files:
                    print(
                        f"  • Nome: {YELLOW}{f.name:<8}{RESET} | Tamanho: {GREEN}{f.size:<3}{RESET} blocos | Bloco Inicial: {CYAN}{f.start_block}{RESET}"
                    )
            input("\nPressione Enter para continuar...")

        elif choice == "4":
            break
        else:
            print(f"{RED}Opção inválida!{RESET}")
            input("\nPressione Enter para continuar...")


def main():
    while True:
        clear_screen()
        print_banner()
        print(f"\n{BOLD}Selecione o cenário ou simulação:{RESET}")
        print(f"  [{GREEN}1{RESET}] Cenário 1: Alocação e Exclusão Simples (Demo)")
        print(f"  [{GREEN}2{RESET}] Cenário 2: Demonstração de Fragmentação Externa (Demo)")
        print(f"  [{GREEN}3{RESET}] Cenário 3: Relatório de Métricas Detalhado (Demo)")
        print(f"  [{GREEN}4{RESET}] Modo de Simulação Interativa (Passo a Passo)")
        print(f"  [{GREEN}5{RESET}] Sair")

        choice = input(f"\n{BOLD}Escolha uma opção (1-5): {RESET}").strip()

        if choice == "1":
            clear_screen()
            print_banner()
            simple_demo.run()
            input("\nPressione Enter para voltar ao menu...")
        elif choice == "2":
            clear_screen()
            print_banner()
            fragmentation_demo.run()
            input("\nPressione Enter para voltar ao menu...")
        elif choice == "3":
            clear_screen()
            print_banner()
            metrics_demo.run()
            input("\nPressione Enter para voltar ao menu...")
        elif choice == "4":
            run_interactive()
        elif choice == "5":
            clear_screen()
            print(f"\n{GREEN}Obrigado por usar o simulador! Até mais.{RESET}\n")
            break
        else:
            print(f"{RED}Opção inválida!{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()
