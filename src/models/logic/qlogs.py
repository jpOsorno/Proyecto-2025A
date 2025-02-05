        omegas_origen = np.array([vertices[0]])
        deltas_origen = np.array(vertices[1:])

        vertices_fase = vertices

        omegas_ciclo = omegas_origen
        deltas_ciclo = deltas_origen
        self.logger.debug(omegas_ciclo, deltas_ciclo)

        # particiones_candidatas = []

        # Se iteran dos veces menos obviando las iteraciones donde no hay particiones y cuando quedarían seleccionados todas las particiones.
        for i in range(len(vertices_fase) - 2):
            self.logger.warn(f"\n{'≡' * 50}{i=}")
            self.logger.debug(
                f"FASE con nuevo grupo formado (si i{NEQ_SYM}0):\n\t{vertices_fase}"
            )

            # asignar de nivel anterior a elementos de omegas
            omegas_ciclo = [vertices_fase[0]]
            deltas_ciclo = vertices_fase[1:]

            self.logger.debug(f"fase inicia con W: {omegas_ciclo}")
            partition_emd = INFTY_POS

            for j in range(len(deltas_ciclo) - 1):
                self.logger.warn(f"\n{'='*45}{j=}")
                self.logger.debug(f"CICLO W crece: {omegas_ciclo}")

                # selección primer elemento de vertices

                local_min_emd = 1e5
                iter_mip: tuple[int, int] | list[tuple[int, int]]
                index_mip: int
                for k in range(len(deltas_ciclo)):
                    self.logger.warn(f"\n{'-'*40}{k=}")
                    self.logger.debug("ITER calculando cada delta")

                    comp_emd, ind_emd, ind_dist = self.funcion_submodular(
                        deltas_ciclo[k], omegas_ciclo
                    )
                    iter_emd = comp_emd - ind_emd

                    self.logger.debug(f"local: {iter_emd}, global: {local_min_emd}")
                    if iter_emd < local_min_emd:
                        local_min_emd = iter_emd
                        iter_mip = deltas_ciclo[k]
                        index_mip = k

                        partition_emd = ind_emd
                        partition_dist = ind_dist
                    else:
                        partition_emd = ind_emd
                        partition_dist = ind_dist

                    ...

                omegas_ciclo.append(deltas_ciclo[index_mip])
                self.logger.debug(
                    f"\nCICLO Minimo delta hallado:\n\t{deltas_ciclo[index_mip]=}"
                )
                self.logger.debug("\tAñadir a ciclo omega. Quitándolo de deltas.")
                deltas_ciclo.pop(index_mip)

                # print(f"{iter_mip=}")
                ...

            # El detalle es que estas uniones de la ultima y penultima parte se encuentran de la memoización en la generación de las particiones individuales, puesto en algún punto se va a evaluar un delta que será la unión de estos dos en la siguiente iteración.
            # #    penultimo_mip, penultima_emd)

            self.logger.debug("Añadir nueva partición entre ultimos de omega y delta")
            self.logger.debug(f"{omegas_ciclo, deltas_ciclo=}")

            self.partition_memory[
                tuple(
                    deltas_ciclo[LAST_IDX]
                    if isinstance(deltas_ciclo[LAST_IDX], list)
                    else deltas_ciclo
                )
            ] = partition_emd, partition_dist

            last_pair = (
                [omegas_ciclo[LAST_IDX]]
                if isinstance(omegas_ciclo[LAST_IDX], tuple)
                else omegas_ciclo[LAST_IDX]
            ) + (
                deltas_ciclo[LAST_IDX]
                if isinstance(deltas_ciclo[LAST_IDX], list)
                else deltas_ciclo  # adición de los dos últimos elementos en uno sólo.
            )

            # self.partition_memory[tuple(last_pair)] = partition_emd

            self.logger.debug(f"{last_pair=}")

            omegas_ciclo.pop()  # quitar el último elemento pues está en el par
            omegas_ciclo.append(last_pair)

            # vertices_fase # cambiarlos y ponerles con el nuevo grupo formado, así cuando vuelva a la fase se repetirá todo igual pero con el grupo en cuenta
            vertices_fase = omegas_ciclo
            ...

        self.logger.warn(
            f"\nGrupos partición obtenidos durante ejecucion:\n{(self.partition_memory)=}"
        )
        # self.logger.warn(f"{self.individual_memory=}")

        return min(self.partition_memory, key=lambda k: self.partition_memory[k][0])
        ...

    def funcion_submodular(
        self, deltas: tuple | list[tuple], omegas: list[tuple | list[tuple]]
    ):
        # Acá lo que se hace es a partir de los elementos que estén en el conjunto omega (W) y delta se creen en esencia, las particiones.
        times = np.copy(self.times)
        individual_emd = INFTY_NEG

        # self.logger.debug(f"{deltas=}")

        # creamos la partición del individual
        if isinstance(deltas, tuple):
            d_time, d_index = deltas
            times[d_time][d_index] = ACTIVOS
        else:
            for delta in deltas:
                d_time, d_index = delta
                times[d_time][d_index] = ACTIVOS

        if tuple(deltas) in self.individual_memory:
            individual_emd, indivector_marginal = self.individual_memory[tuple(deltas)]
        else:
            individual = self.sia_subsistema

            # self.logger.info(f"{times[EFECTO], times[ACTUAL]=}")

            dims_efecto_ind = tuple(
                idx for idx, bit in enumerate(times[EFECTO]) if bit == INT_ONE
            )
            dims_presente_ind = tuple(
                idx for idx, bit in enumerate(times[ACTUAL]) if bit == INT_ONE
            )

            ind_part = individual.bipartir(
                np.array(dims_efecto_ind, dtype=np.int8),
                np.array(dims_presente_ind, dtype=np.int8),
            )
            indivector_marginal = ind_part.distribucion_marginal()
            individual_emd = emd_efecto(indivector_marginal, self.sia_dists_marginales)

            self.individual_memory[tuple(deltas)] = individual_emd, indivector_marginal

            # self.logger.debug(f"{self.sia_dists_marginales=}")
            # self.logger.debug(f"{indivector_marginal=}")

            # memoizamos el individuo
            # self.logger.info(f"{individual_emd}")

            # self.logger.info("ind_part")
            # self.logger.info(f"{ind_part}")

        # Luego lo hacemos para los omegas
        for omega in omegas:
            if isinstance(omega, list):
                for omg in omega:
                    o_time, o_index = omg
                    times[o_time][o_index] = ACTIVOS
            else:
                o_time, o_index = omega
                times[o_time][o_index] = ACTIVOS

        combinacion = self.sia_subsistema

        dims_efecto_comb = tuple(
            idx for idx, bit in enumerate(times[EFECTO]) if bit == INT_ONE
        )
        dims_presente_comb = tuple(
            idx for idx, bit in enumerate(times[ACTUAL]) if bit == INT_ONE
        )

        comb_part = combinacion.bipartir(
            np.array(dims_efecto_comb, dtype=np.int8),
            np.array(dims_presente_comb, dtype=np.int8),
        )
        comvector_marginal = comb_part.distribucion_marginal()
        combinada_emd = emd_efecto(comvector_marginal, self.sia_dists_marginales)

        # self.logger.debug(f"{omegas=}")

        # self.logger.info(f"{times[EFECTO], times[ACTUAL]=}")
        # self.logger.info("comb_part")
        # self.logger.info(f"{comb_part}")

        # self.logger.debug(f"{self.sia_dists_marginales=}")
        # self.logger.debug(f"{comvector_marginal=}")

        # self.logger.debug(
        #     f"{combinada_emd - individual_emd}={combinada_emd}-{individual_emd}"
        # )

        return combinada_emd, individual_emd, indivector_marginal

    def view_solution(self, mip: tuple[tuple[int, int]]):
        times = ([], [])
        complement = self.vertices - set(mip)
        for part_prim in mip:
            time, index = part_prim
            letter = self.labels[time][index]
            # ponemos en la parte primal (1)
            times[0].append(letter)

        for part_dual in complement:
            time, index = part_dual
            letter = self.labels[time][index]
            # ponemos en la parte dual (1)
            times[1].append(letter)

        # self.logger.debug(f"{times, self.memory[mip]=}")
        # self.logger.debug(f"{mip=}")
        biparticion_fmt = fmt_biparte_q(times[0], times[1])
        return biparticion_fmt
        print(f"{mip=}")

    def nodes_complement(self, nodes: list[tuple[int, int]]):
        return list(set(self.vertices) - set(nodes))

